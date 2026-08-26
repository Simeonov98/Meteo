"""One dataclass per forecast source, matching that source's DB table 1:1.

The three sites expose different fields (rain vs. humidity, an imageId
column on Sinoptik, etc.), so a single shared "Forecast" type would need a
pile of source-specific optional fields. Keeping them separate mirrors the
actual schema and keeps each scraper's output self-explanatory.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# "imageId" is NOT NULL on all three tables but nothing populates a real
# Image row per forecast (see docs/image-capture.md for why, and how to
# properly wire one up later). 0 is a safe placeholder: there's no foreign
# key on imageId, so it doesn't need to reference a real Image row.
NO_IMAGE_ID = 0


@dataclass
class FreemeteoForecast:
    forecast_day: date
    weekday: int
    tmax: float
    tmin: float
    text: str
    wdir: str
    rain: str
    city_id: int
    image_id: int = NO_IMAGE_ID


@dataclass
class DalivaliForecast:
    forecast_day: date
    weekday: int
    tmax: float
    tmin: float
    wspd: str
    wdir: str
    humidity: str
    text: str
    city_id: int
    image_id: int = NO_IMAGE_ID


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
    image_id: int = NO_IMAGE_ID
