from datetime import date

import pytest

from meteo.utils import (
    degrees_to_compass,
    month_name_to_number,
    next_occurrence_of_weekday,
    weekday_index,
)


@pytest.mark.parametrize(
    "degrees,expected",
    [
        (0, "n"),
        (22, "n"),
        (23, "ne"),
        (46, "ne"),
        (90, "e"),
        (180, "s"),
        (270, "w"),
        (359, "n"),
        (360 + 90, "e"),  # wraps around
    ],
)
def test_degrees_to_compass(degrees, expected):
    assert degrees_to_compass(degrees) == expected


def test_month_name_to_number():
    assert month_name_to_number("октомври") == 10
    assert month_name_to_number("Януари") == 1


def test_month_name_to_number_unknown():
    with pytest.raises(ValueError):
        month_name_to_number("notamonth")


def test_weekday_index_named_day():
    assert weekday_index("Сряда") == 2


def test_weekday_index_today_and_tomorrow():
    monday = date(2024, 1, 1)  # a Monday
    assert weekday_index("Днес", today=monday) == 0
    assert weekday_index("Утре", today=monday) == 1


def test_weekday_index_unknown():
    with pytest.raises(ValueError):
        weekday_index("notaday")


def test_next_occurrence_of_weekday_same_day_returns_today():
    monday = date(2024, 1, 1)
    assert next_occurrence_of_weekday("Понеделник", today=monday) == monday


def test_next_occurrence_of_weekday_later_in_week():
    monday = date(2024, 1, 1)
    assert next_occurrence_of_weekday("Сряда", today=monday) == date(2024, 1, 3)


def test_next_occurrence_of_weekday_wraps_to_next_week():
    friday = date(2024, 1, 5)
    assert next_occurrence_of_weekday("Понеделник", today=friday) == date(2024, 1, 8)
