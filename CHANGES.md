# v1 -> v2

## Structure

- Flat scripts at repo root -> installable package at `src/meteo/`, plus
  `pyproject.toml` (`pip install -e ".[dev]"`, console script `meteo`).
- `main.py` hardcoded 9 calls (3 cities x 3 sources) with inline URLs and
  magic city-id numbers -> `config.py` holds a `City` registry (slug, name,
  id, one URL per source); `cli.py` loops over it and supports
  `--city`/`--source` filters to run a subset.
- Three near-duplicate `numbers_to_strings` dicts and two duplicate
  weekday-parsing functions in `dalivali2.py` -> one shared `utils.py`
  (`MONTHS_BG`, `WEEKDAYS_BG`, `weekday_index`, `next_occurrence_of_weekday`,
  `degrees_to_compass`).
- Three DB modules (`db.py` MySQL, `db2.py` and `db3.py` both Postgres,
  only `db3.py` actually used) -> one `db.py`, Postgres only.

## Correctness fixes

- **SQL injection / broken-query risk**: every insert was built with
  f-strings (`VALUES ('{text[i]}', ...)`). Scraped weather text containing
  an apostrophe would break the query or worse. v2 uses parameterized
  queries (`cur.executemany(query, params)`) everywhere.
- **Dead env var reads**: `db3.py` read `HOST`/`DATABASE`/`DB_USERNAME`/
  `PASSWORD`/`SSL_CERT`, none of which exist in `.env` (which defines
  `PGHOST`/`PGDATABASE`/`PGUSER`/`PGPASSWORD`/`PGSSLMODE`). It happened to
  work anyway because passing `None` to `psycopg2.connect()` lets libpq
  fall back to reading those exact `PG*` variables from the process
  environment. v2's `settings.py` reads the real variable names explicitly.
- Connections were opened and closed per query -> v2 uses a small
  connection pool (`db.py: _get_pool()`), reused across all city/source
  combinations in one run.

## Removed dead code / dead weight

- `chromedriver.exe` (12MB binary) and the `chromedriver-py` dependency:
  every scraper uses Firefox/geckodriver; nothing in the project ever used
  Chrome.
- Sinoptik's per-day icon screenshot -> MD5 hash -> write to a hardcoded
  `/home/simeon/programming/Meteo/sinoptik/...` path (broken on any other
  machine) -> looked up via `SELECT id FROM "Image" WHERE name = ...` for
  the `imageId` column. Nothing ever inserted rows into `Image`, so that
  lookup always returned NULL. v2 drops the screenshot/hash/file-write
  entirely and leaves `imageId` unset — same net result, no side effects.
  `hash.py` (and its unused `numpy` import) is gone with it.
- `freemeteoNew.py`'s `numbers_to_strings` dict was defined but never
  called in the live code path (dates were already parsed via
  `strptime`) — dropped.
- Unused/legacy scripts (`dalivali.py`, `freemeteo.py`, `db.py`, `db2.py`,
  `scraper1.py`, `test.py`, `testFree.py`, `requierments.txt`) moved to
  `archive/` rather than deleted outright, so nothing is lost.
- `__pycache__/*.pyc`, `chromedriver.exe`, and `geckodriver.log` were
  tracked in git despite being listed in `.gitignore` (added after the
  fact) — untracked in v2.

## Other

- `print()` calls -> `logging`, with `--log-level` on the CLI.
- Bare `try/except: pass` and blind `implicitly_wait()` around
  consent-banner clicks -> explicit `WebDriverWait`/`expected_conditions`
  with a bounded timeout.
- Each scraper now separates "scrape into typed dataclasses" (`scrape()`)
  from "write to DB" (`run()`), and driver lifecycle is a context manager
  (`browser.firefox_driver()`) so a mid-scrape exception can't leak an open
  Firefox process.
- Added `tests/` (pytest) covering the pure-logic pieces: wind-degree ->
  compass conversion, BG month/weekday parsing, city registry lookups. The
  scrapers themselves still need a live browser + live site, so they're
  not unit tested — same as before.

## What's unchanged on purpose

- Still Selenium + headless Firefox: all three sites render forecast data
  client-side, so a browser is genuinely needed, not just legacy inertia.
- The scrapers still depend on the sites' current CSS classes / XPath
  structure (especially freemeteo.bg's absolute XPath) — that coupling is
  inherent to scraping pages with no stable selectors, not something a
  rewrite can fix without the sites offering a real API.
- DB table/column names are untouched (`"Freemeteo"`, `"Dalivali"`,
  `"Sinoptik"`, `forecastDay`/`forecastDate`, `cityId`, etc.) since this
  writes into your existing production schema.
