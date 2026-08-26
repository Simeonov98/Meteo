"""Scrapes the next few days' forecast from freemeteo.bg.

As of 2026-08, the "15-days/list" page's own forecast section
(`section.fifteen-day-forecast`) is a Recharts SVG trend chart that only
exposes date + max temp -- no min temp, wind, rain, or description. The
per-day detail this scraper needs (and the site still fully renders) lives
in the day-selector strip above it: one `<a href="/weather/.../hourly-
forecast/dayN/">` per upcoming day, each carrying date, both temps, a
weather-icon `title` (description), a wind icon whose inline
`transform: rotate(...)` gives direction, and a `data-precipitation`
attribute. That's what this scrapes instead.

Two quirks in that strip:
- It also contains plain nav links ("Почасово" tab buttons) that reuse the
  same `/today/`-ish hrefs but carry no forecast data -- so cards are
  identified by "has a forecast icon", not by href pattern.
- Tomorrow's card is labeled "Утре" instead of a "DD MM" date (today's
  would be "Днес", but today is always skipped). Every other card has a
  real date. This is the same quirk the pre-rewrite scraper special-cased
  for the old page layout -- it's still there, just on different markup.

Each day link's markup contains two copies of this info (a `md:hidden`
mobile layout and a `hidden md:flex` desktop layout, both always in the
DOM). We force a wide window so only the desktop layout is visible --
`.innerText` only reflects visible elements, so this keeps date/temp
parsing to one clean line per field. Everything else here (icon title,
rain, wind svg) is read via explicit selectors/attributes rather than
`.innerText` position, which are identical in both copies regardless of
which one is visible.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from meteo import db
from meteo.browser import firefox_driver
from meteo.config import City
from meteo.models import FreemeteoForecast
from meteo.utils import degrees_to_compass

logger = logging.getLogger(__name__)

_DAY_LINK_SELECTOR = "a[href*='hourly-forecast/']"
_CONSENT_BUTTON_CLASS = "fc-button-label"
_DAYS_TO_READ = 5
# Wide enough to keep the site above its `md:` breakpoint, so each day card
# renders (and reports in .innerText) as a single desktop-layout block.
_WINDOW_SIZE = (1400, 1000)


def _dismiss_consent(driver) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, _CONSENT_BUTTON_CLASS))
        ).click()
    except TimeoutException:
        pass


def _is_day_card(link) -> bool:
    return bool(link.find_elements(By.CSS_SELECTOR, "img[data-forecast-code]"))


def _resolve_forecast_date(date_prefix: list[str]) -> datetime:
    if date_prefix == ["Утре"]:
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    _weekday_name, date_str = date_prefix
    return datetime.strptime(date_str, "%d %m").replace(year=datetime.now().year)


def _parse_day_card(day) -> dict:
    # Normal day: ['четвъртък', '27 08', 'предимно ясно.', '31°', '20°', '29°', '16 км/ч', '0мм']
    # Tomorrow:   ['Утре', 'частична заоблаченост.', '29°', '20°', '26°', '13 км/ч', '0.4мм']
    # The last 6 lines are always [text, tmax, tmin, <feels-like tooltip>, windspeed, rain];
    # everything before that is the weekday/date label.
    lines = [line for line in day.get_attribute("innerText").split("\n") if line.strip()]
    date_prefix, (_text, tmax, tmin, _feels_like, _wspd, _rain) = lines[:-6], lines[-6:]

    icon = day.find_element(By.CSS_SELECTOR, "img[data-forecast-code]")
    rain_el = day.find_element(By.CSS_SELECTOR, "[data-precipitation]")
    wind_svg = day.find_element(By.CSS_SELECTOR, "svg[style*='rotate']")
    degrees = float(wind_svg.get_attribute("style").split("rotate(")[1].split("deg)")[0])

    return {
        "forecast_date": _resolve_forecast_date(date_prefix),
        "tmax": float(tmax.rstrip("°")),
        "tmin": float(tmin.rstrip("°")),
        "text": icon.get_attribute("title"),
        "wind_dir": degrees_to_compass(degrees),
        "rain": rain_el.get_attribute("data-precipitation"),
    }


def scrape(driver, url: str, city_id: int) -> list[FreemeteoForecast]:
    driver.set_window_size(*_WINDOW_SIZE)
    driver.get(url)
    _dismiss_consent(driver)

    links = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, _DAY_LINK_SELECTOR))
    )
    day_cards = [link for link in links if _is_day_card(link)]
    # First card is always today, which we skip -- start from tomorrow.
    days = day_cards[1 : 1 + _DAYS_TO_READ]

    forecasts = []
    for day in days:
        card = _parse_day_card(day)
        forecast_date = card["forecast_date"]
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
