"""Shared parsing helpers for turning Bulgarian-language forecast text into
typed values. Centralized here because the original scrapers each redefined
their own (slightly inconsistent) copies of these lookups.
"""

from __future__ import annotations

from datetime import date, timedelta

WEEKDAYS_BG = [
    "Понеделник",
    "Вторник",
    "Сряда",
    "Четвъртък",
    "Петък",
    "Събота",
    "Неделя",
]

MONTHS_BG = {
    "януари": 1,
    "февруари": 2,
    "март": 3,
    "април": 4,
    "май": 5,
    "юни": 6,
    "юли": 7,
    "август": 8,
    "септември": 9,
    "октомври": 10,
    "ноември": 11,
    "декември": 12,
}

_COMPASS_POINTS = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]


def degrees_to_compass(degrees: float) -> str:
    """Convert a wind bearing in degrees to one of 8 compass directions."""
    index = int(((degrees % 360) + 22.5) // 45) % 8
    return _COMPASS_POINTS[index]


def month_name_to_number(name: str) -> int:
    """Look up a full Bulgarian month name, e.g. 'октомври' -> 10."""
    try:
        return MONTHS_BG[name.lower()]
    except KeyError:
        raise ValueError(f"Unknown Bulgarian month name: {name!r}") from None


def weekday_index(day_name: str, today: date | None = None) -> int:
    """Resolve a Bulgarian weekday name (or 'Днес'/'Утре') to 0=Monday..6=Sunday."""
    today = today or date.today()
    if day_name == "Днес":
        return today.weekday()
    if day_name == "Утре":
        return (today.weekday() + 1) % 7
    try:
        return WEEKDAYS_BG.index(day_name)
    except ValueError:
        raise ValueError(f"Unknown Bulgarian weekday name: {day_name!r}") from None


def next_occurrence_of_weekday(day_name: str, today: date | None = None) -> date:
    """Resolve a Bulgarian weekday name (or 'Днес'/'Утре') to the next matching date."""
    today = today or date.today()
    target = weekday_index(day_name, today)
    days_ahead = (target - today.weekday()) % 7
    return today + timedelta(days=days_ahead)
