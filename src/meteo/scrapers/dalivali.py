"""Scrapes the 7-day forecast table from dalivali.bg."""

from __future__ import annotations

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from meteo import db
from meteo.browser import firefox_driver
from meteo.config import City
from meteo.models import DalivaliForecast
from meteo.utils import next_occurrence_of_weekday, weekday_index

logger = logging.getLogger(__name__)

_CONSENT_BUTTON_SELECTOR = ".fc-cta-consent"
_FORECAST_TABLE_XPATH = "/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[2]"
_ROWS_TO_READ = 7


def _dismiss_consent(driver) -> None:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, _CONSENT_BUTTON_SELECTOR))
    ).click()


def _parse_row(row) -> dict:
    day_name = row.find_element(By.CLASS_NAME, "day").get_attribute("innerText").split()[0]
    temps = row.find_element(By.CLASS_NAME, "info-data").find_element(By.ID, "temp-today")
    temp_parts = temps.get_attribute("innerText").split()
    wind_speed = row.find_element(By.CLASS_NAME, "info-data").find_element(By.ID, "wind-today")
    wind_dir = row.find_element(By.CLASS_NAME, "info-data").find_element(By.ID, "dr-today")
    humidity = row.find_element(By.CLASS_NAME, "info-data").find_element(By.ID, "rain-today")
    text = row.find_element(By.CLASS_NAME, "icon-forecast").find_element(By.TAG_NAME, "img")

    return {
        "day_name": day_name,
        "tmin": temp_parts[0],
        "tmax": temp_parts[2],
        "wind_speed": f"{wind_speed.get_attribute('innerText')} m/s",
        "wind_dir": wind_dir.get_attribute("innerText").split()[0],
        "humidity": humidity.get_attribute("innerText"),
        "text": text.get_attribute("title"),
    }


def scrape(driver, url: str, city_id: int) -> list[DalivaliForecast]:
    driver.get(url)
    _dismiss_consent(driver)

    forecast_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, _FORECAST_TABLE_XPATH))
    )
    rows = forecast_table.find_elements(By.CLASS_NAME, "row")[2 : 2 + _ROWS_TO_READ]

    forecasts = []
    for row in rows:
        parsed = _parse_row(row)
        forecast_date = next_occurrence_of_weekday(parsed["day_name"])
        forecasts.append(
            DalivaliForecast(
                forecast_day=forecast_date,
                weekday=weekday_index(parsed["day_name"]),
                tmax=float(parsed["tmax"]),
                tmin=float(parsed["tmin"]),
                wspd=parsed["wind_speed"],
                wdir=parsed["wind_dir"],
                humidity=parsed["humidity"],
                text=parsed["text"],
                city_id=city_id,
            )
        )
    return forecasts


def run(city: City, *, headless: bool = True) -> int:
    logger.info("dalivali: scraping %s", city.name)
    with firefox_driver(headless=headless) as driver:
        forecasts = scrape(driver, city.dalivali_url, city.city_id)
    return db.insert_dalivali(forecasts)
