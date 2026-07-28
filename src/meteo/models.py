"""One dataclass per forecast source, matching that source's DB table 1:1.

The three sites expose different fields (rain vs. humidity, an imageId
column on Sinoptik, etc.), so a single shared "Forecast" type would need a
pile of source-specific optional fields. Keeping them separate mirrors the
actual schema and keeps each scraper's output self-explanatory.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class FreemeteoForecast:
    forecast_day: date
    weekday: int
    tmax: float
    tmin: float
    text: str
    wdir: str
    rain: float
    city_id: int


@dataclass
class DalivaliForecast:
    forecast_day: date
    weekday: int
    tmax: float
    tmin: float
    wspd: str
    wdir: str
    humidity: str
    city_id: int


@dataclass
class SinoptikForecast:
    forecast_date: date
    weekday: int
    tmax: float
    tmin: float
    wdir: str
    wspd: str
    text: str
    city_id: int
