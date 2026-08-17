"""Static registry of tracked cities and their per-source forecast URLs.

Adding a new city means adding one entry here -- nothing else in the
codebase hardcodes city names, ids, or URLs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    slug: str
    name: str
    city_id: int
    freemeteo_url: str
    dalivali_url: str
    sinoptik_url: str


CITIES: dict[str, City] = {
    "plovdiv": City(
        slug="plovdiv",
        name="Plovdiv",
        city_id=5,
        freemeteo_url="https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria",
        dalivali_url="https://dalivali.bg/?location=173",
        sinoptik_url="https://www.sinoptik.bg/plovdiv-bulgaria-100728193/14-days/",
    ),
    "sofia": City(
        slug="sofia",
        name="Sofia",
        city_id=6,
        freemeteo_url="https://freemeteo.bg/weather/sofia/15-days/list/?gid=727011&language=bulgarian&country=bulgaria",
        dalivali_url="https://dalivali.bg/?location=217",
        sinoptik_url="https://www.sinoptik.bg/sofia-bulgaria-100727011/14-days",
    ),
    "vidin": City(
        slug="vidin",
        name="Vidin",
        city_id=7,
        freemeteo_url="https://freemeteo.bg/weather/vidin/15-days/list/?gid=725905&language=bulgarian&country=bulgaria",
        dalivali_url="https://dalivali.bg/?location=48",
        sinoptik_url="https://www.sinoptik.bg/vidin-bulgaria-100725905/14-days",
    ),
}

SOURCES = ("freemeteo", "dalivali", "sinoptik")


def get_cities(slugs: list[str] | None = None) -> list[City]:
    """Look up cities by slug, preserving CITIES' order when slugs is None."""
    if not slugs:
        return list(CITIES.values())
    unknown = set(slugs) - CITIES.keys()
    if unknown:
        raise KeyError(f"Unknown city slug(s): {', '.join(sorted(unknown))}")
    return [CITIES[slug] for slug in slugs]
