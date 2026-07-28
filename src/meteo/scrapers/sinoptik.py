"""Scrapes the 14-day forecast panel from sinoptik.bg.

The original version also screenshotted each day's weather icon, MD5-hashed
it, and wrote it to a hardcoded local path (`/home/simeon/programming/...`,
broken on any other machine) so it could look up a matching row in an
`Image` table -- but nothing ever inserted rows into that table, so the
lookup always resolved to NULL. That whole side effect was dead weight and
is dropped here; `imageId` is simply left unset on insert.
"""

from __future__ import annotations

import logging
from datetime import date, datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from meteo import db
from meteo.browser import firefox_driver
from meteo.config import City
from meteo.models import SinoptikForecast
from meteo.utils import month_name_to_number

logger = logging.getLogger(__name__)

_CONSENT_BUTTON_ID = "didomi-notice-agree-button"
_DAYS_CONTAINER_CLASS = "wf14dayRightContent"
_DAYS_TO_READ = 7


def _dismiss_consent(driver) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, _CONSENT_BUTTON_ID))
        ).click()
    except TimeoutException:
        pass


def _parse_date(raw_date: str) -> date:
    day_str, month_name = raw_date.split()[:2]
    return date(datetime.now().year, month_name_to_number(month_name), int(day_str))


def _parse_day(day) -> dict:
    return {
        "date": day.find_element(By.CLASS_NAME, "wf10dayRightDate").get_attribute("innerHTML"),
        "tmax": day.find_element(By.CLASS_NAME, "wf10dayRightTemp").text,
        "tmin": day.find_element(By.CLASS_NAME, "wf10dayRightTempLow").text,
        "wind_dir": day.find_element(By.CLASS_NAME, "wf10dayRightWind").get_attribute("title"),
        "wind_speed": day.find_element(By.CLASS_NAME, "wf10dayRightWind").text,
        "text": day.find_element(By.CLASS_NAME, "wf10dayRightImg").get_attribute("title"),
    }


def scrape(driver, url: str, city_id: int) -> list[SinoptikForecast]:
    driver.get(url)
    _dismiss_consent(driver)

    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, _DAYS_CONTAINER_CLASS))
    )
    days = container.find_elements(By.TAG_NAME, "a")[:_DAYS_TO_READ]

    forecasts = []
    for day in days:
        parsed = _parse_day(day)
        forecast_date = _parse_date(parsed["date"])
        forecasts.append(
            SinoptikForecast(
                forecast_date=forecast_date,
                weekday=forecast_date.weekday(),
                tmax=float(parsed["tmax"].rstrip("°")),
                tmin=float(parsed["tmin"].rstrip("°")),
                wdir=parsed["wind_dir"],
                wspd=parsed["wind_speed"],
                text=parsed["text"],
                city_id=city_id,
            )
        )
    return forecasts


def run(city: City, *, headless: bool = True) -> int:
    logger.info("sinoptik: scraping %s", city.name)
    with firefox_driver(headless=headless) as driver:
        forecasts = scrape(driver, city.sinoptik_url, city.city_id)
    return db.insert_sinoptik(forecasts)
