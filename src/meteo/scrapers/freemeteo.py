"""Scrapes the 5-day forecast list from freemeteo.bg.

The page has no stable class names for the per-day cards, so this still
relies on an absolute XPath into the forecast section -- that coupling to
the live page structure is inherent to the site, not something a rewrite
can clean up.
"""

from __future__ import annotations

import logging
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from meteo import db
from meteo.browser import firefox_driver
from meteo.config import City
from meteo.models import FreemeteoForecast
from meteo.utils import degrees_to_compass, parse_tomorrow_label

logger = logging.getLogger(__name__)

_DAY_CARD_XPATH = "/html/body/div[3]/div[2]/section[2]/div/div[{index}]"
_CONSENT_BUTTON_CLASS = "fc-button-label"
_DAYS_TO_READ = 5


def _dismiss_consent(driver) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, _CONSENT_BUTTON_CLASS))
        ).click()
    except TimeoutException:
        pass


def _parse_day_card(driver, index: int) -> dict:
    day = driver.find_element(By.XPATH, _DAY_CARD_XPATH.format(index=index))
    wind_svg = day.find_element(By.CSS_SELECTOR, "svg[data-testid='IcWindIcon']")
    style = wind_svg.get_attribute("style")
    degrees = float(style.split("rotate(")[1].split("deg)")[0])

    lines = [line for line in day.get_attribute("innerText").split("\n") if line.strip()]
    if lines[0] == "Утре":
        # ['Утре', 'частична заоблаченост.', '29°', '17°', '8 км/ч', '0мм']
        title, text, tmax, tmin, rain = lines[0], lines[1], lines[2], lines[3], lines[5]
    else:
        # ['сряда', '10 09', 'частична заоблаченост.', '31°', '19°', '11 км/ч', '0мм']
        title = f"{lines[0]}, {lines[1]}"
        text, tmax, tmin, rain = lines[2], lines[3], lines[4], lines[6]

    return {
        "title": title,
        "text": text,
        "tmax": float(tmax.rstrip("°")),
        "tmin": float(tmin.rstrip("°")),
        "wind_dir": degrees_to_compass(degrees),
        "rain": float(rain.replace(",", ".").rstrip("мм")),
    }


def _resolve_forecast_date(title: str) -> datetime:
    if title == "Утре":
        tomorrow = parse_tomorrow_label()
        return datetime(datetime.now().year, datetime.now().month, tomorrow.day)
    _, day_month = title.split(", ")
    return datetime.strptime(day_month, "%d %m").replace(year=datetime.now().year)


def scrape(driver, url: str, city_id: int) -> list[FreemeteoForecast]:
    driver.get(url)
    _dismiss_consent(driver)

    cards = [_parse_day_card(driver, i) for i in range(3, 3 + _DAYS_TO_READ)]
    forecasts = []
    for card in cards:
        forecast_date = _resolve_forecast_date(card["title"])
        forecasts.append(
            FreemeteoForecast(
                forecast_day=forecast_date,
                weekday=forecast_date.weekday(),
                tmax=card["tmax"],
                tmin=card["tmin"],
                text=card["text"],
                wdir=card["wind_dir"],
                rain=card["rain"],
                city_id=city_id,
            )
        )
    return forecasts


def run(city: City, *, headless: bool = True) -> int:
    logger.info("freemeteo: scraping %s", city.name)
    with firefox_driver(headless=headless) as driver:
        forecasts = scrape(driver, city.freemeteo_url, city.city_id)
    return db.insert_freemeteo(forecasts)
