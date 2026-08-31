"""One dataclass per forecast source, matching that source's DB table 1:1.

The three sites expose different fields (rain vs. humidity, an imageId
column on Sinoptik, etc.), so a single shared "Forecast" type would need a
pile of source-specific optional fields. Keeping them separate mirrors the
actual schema and keeps each scraper's output self-explanatory.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# "imageId" is NOT NULL (and, in production, has a real foreign key against
# "Image") on all three tables, but nothing populates a real Image row per
# forecast (see docs/image-capture.md for why, and how to properly wire one
# up later). 0 is a sentinel meaning "no real image" -- db.py resolves it to
# a get-or-create placeholder Image row before insert, since it can't be
# used as a literal value wherever the foreign key is enforced.
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
