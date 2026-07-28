from __future__ import annotations

import argparse
import logging
import sys

from meteo import db
from meteo.config import SOURCES, get_cities
from meteo.scrapers import SCRAPERS

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="meteo", description=__doc__)
    parser.add_argument(
        "--city",
        action="append",
        dest="cities",
        metavar="SLUG",
        help="Limit to a city slug (plovdiv/sofia/vidin); repeatable. Default: all.",
    )
    parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        choices=SOURCES,
        metavar="SOURCE",
        help="Limit to a forecast source; repeatable. Default: all.",
    )
    parser.add_argument(
        "--no-headless",
        action="store_false",
        dest="headless",
        default=True,
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument("--log-level", default="INFO")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=args.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    try:
        cities = get_cities(args.cities)
    except KeyError as exc:
        logger.error(str(exc))
        return 1

    sources = args.sources or list(SOURCES)

    failures = 0
    for city in cities:
        for source in sources:
            try:
                count = SCRAPERS[source].run(city, headless=args.headless)
                logger.info("%s/%s: wrote %d rows", source, city.slug, count)
            except Exception:
                failures += 1
                logger.exception("%s/%s: scrape failed", source, city.slug)

    db.close_pool()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
