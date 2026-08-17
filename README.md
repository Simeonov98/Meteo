# Meteo

Meteo scrapes multi-day weather forecasts from three Bulgarian weather sites
(freemeteo.bg, dalivali.bg, sinoptik.bg) for Plovdiv, Sofia, and Vidin, and
stores them in Postgres. The goal is to compare each site's forecast against
what actually happened, as the gap between prediction and forecast date
shrinks.

This is v2: a structural rewrite of the original scraper scripts. See
[CHANGES.md](CHANGES.md) for what changed and why. The pre-rewrite scripts
still live in [archive/](archive/) for reference.

## Project layout

```
src/meteo/
  config.py      city/URL registry
  models.py      one dataclass per forecast source, matching its DB table
  utils.py       BG weekday/month/wind-direction parsing helpers
  settings.py    .env / environment variable loading
  db.py          Postgres access (parameterized queries, connection pool)
  browser.py     headless Firefox driver setup
  scrapers/      one module per source: freemeteo.py, dalivali.py, sinoptik.py
  cli.py         command-line entry point
tests/           unit tests for the pure-logic pieces (utils, config)
archive/         pre-rewrite scripts, kept for reference only
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in PGHOST / PGDATABASE / PGUSER / PGPASSWORD
```

## Usage

```bash
python main.py                              # scrape all cities, all sources
python main.py --city sofia --city plovdiv  # only these cities
python main.py --source sinoptik            # only this source
python main.py --no-headless                # show the browser window
```

Equivalent to running the installed console script: `meteo ...`.

## Tests

```bash
pytest
```

Only the pure-logic modules (date/weekday/wind parsing, city config) are
unit tested. The scrapers themselves drive a real browser against live
sites and aren't covered by automated tests.
