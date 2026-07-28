import pytest

from meteo.config import CITIES, get_cities


def test_get_cities_defaults_to_all():
    assert get_cities(None) == list(CITIES.values())


def test_get_cities_filters_by_slug():
    result = get_cities(["sofia"])
    assert [c.slug for c in result] == ["sofia"]


def test_get_cities_unknown_slug_raises():
    with pytest.raises(KeyError):
        get_cities(["atlantis"])


def test_every_city_has_urls_for_all_sources():
    for city in CITIES.values():
        assert city.freemeteo_url.startswith("https://")
        assert city.dalivali_url.startswith("https://")
        assert city.sinoptik_url.startswith("https://")
