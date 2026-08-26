# v2 rollout notes — what happened after the rewrite

This covers everything from "the v2 rewrite is written" to "it actually
runs and writes correct data," across getting it running locally, wiring
up GitHub Actions, and the real data bugs found along the way. Written
because most of this isn't visible from the code alone — it's the story of
*why* things ended up the way they are.

## 1. Local environment: the SSL/geckodriver saga

Running `python main.py` first failed with `ModuleNotFoundError: No module
named 'meteo'` — the package was never `pip install -e`'d into the actual
project `.venv` (only tested in a throwaway venv earlier). Fixed with:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

Next failure: `webdriver_manager.GeckoDriverManager().install()` (in the
original `browser.py`) crashed with `ssl.SSLEOFError` trying to reach
`api.github.com`. Root cause: `.venv`'s Python 3.9.6 is Apple's Xcode
Command Line Tools build, linked against old **LibreSSL 2.8.3**, not
OpenSSL. `urllib3` v2 (pulled in by `requests`, used by
`webdriver-manager`, required transitively by `selenium>=4.20`) dropped
support for anything but OpenSSL 1.1.1+. That's the `NotOpenSSLWarning`
printed at the top of every run — it's the actual cause, not noise.

Fix (you applied this directly): install geckodriver via Homebrew so
Selenium never needs to phone GitHub for it:
```bash
brew install geckodriver
```
and simplified `src/meteo/browser.py` to `webdriver.Firefox(service=
FirefoxService(), options=options)` — no explicit driver path. In practice
Selenium's own bundled **Selenium Manager** resolves the browser/driver
pair and found the Homebrew-installed geckodriver on `PATH` automatically
— confirmed via debug logs (`Found geckodriver 0.37.1 in PATH:
/opt/homebrew/bin/geckodriver`). `webdriver-manager` is no longer used;
its dependency line in `pyproject.toml` is commented out (not deleted, in
case you want it back).

Also: `requires-python` in `pyproject.toml` was originally `>=3.10`, which
doesn't match this machine's actual Python (3.9.6). Per your instruction
("no need to upgrade Python, use the system one"), this was lowered to
`>=3.9` rather than installing a newer interpreter. All type hints use
`from __future__ import annotations` so PEP 604 `X | None` syntax still
works at runtime on 3.9.

**Net effect**: no changes needed to your actual system Python. Only
addition to the machine: `geckodriver` via Homebrew.

## 2. GitHub Actions

Added `.github/workflows/scrape.yml`: runs `python main.py` on
`ubuntu-latest` (which ships with Firefox + geckodriver preinstalled, so
the same PATH-based driver resolution works there for free, no CI-specific
code needed).

- **Secrets**: needs 5 separate repo secrets (Settings → Secrets and
  variables → Actions): `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`,
  `PGSSLMODE` — one each, not bundled, since the workflow references them
  individually and there's no built-in secret-parsing step that would
  make bundling worthwhile.
- **Trigger**: originally set to run hourly via `cron: "0 * * * *"`. You
  later commented that out yourself (commit `7578017`) — only
  `workflow_dispatch` (the manual "Run workflow" button in the Actions tab)
  is currently active. **The scheduled run is OFF right now.** To turn it
  back on, uncomment the `schedule:` block in
  `.github/workflows/scrape.yml`.
- **Important caveat if you re-enable the schedule**: GitHub only fires
  `schedule:` triggers for workflow files that exist on the repo's
  **default branch** (`main`). Right now everything is on the local `v2`
  branch, which hasn't even been pushed to GitHub yet — so the workflow
  currently can't run at all (scheduled or manual) until `v2` is pushed,
  and cron specifically won't fire until it's on `main`.
- Nothing has been pushed to `origin` (GitHub) at any point in this
  session. Everything so far is local-only, across 3 commits on `v2`
  (`e02ad55`, `f3d0699`, `7578017`) plus a batch of uncommitted fixes from
  section 3 below.

## 3. Data bugs found while actually running it against the real DB

Once it ran, DB inserts started failing with real constraint violations —
these weren't v2 regressions, they were **pre-existing bugs v1 never
surfaced** because `archive/db3.py`'s `push()` swallowed every exception
with a bare `print()` instead of raising. v2 raising errors properly is
what exposed all three of these:

**a) `imageId` is NOT NULL on all three tables** (`Freemeteo`, `Dalivali`,
`Sinoptik`), confirmed via `information_schema` — and there's no foreign
key on it. v1's screenshot → hash → insert-into-`Image` → lookup pipeline
had its actual insert step commented out, so that lookup always resolved
to `NULL` and **every insert on every source has likely always failed in
v1**, silently. Fix: each forecast dataclass now has `image_id` defaulting
to a sentinel `NO_IMAGE_ID = 0` (`src/meteo/models.py`) — safe since
nothing enforces it references a real row. Full write-up of how to
properly bring back real image capture, if you ever want it, is in
[docs/image-capture.md](image-capture.md).

**b) Dalivali's `text` column is NOT NULL**, but v1's scraper never
scraped any description text at all. Found it live: each day's weather
icon on dalivali.bg has a `title` attribute holding the description
(e.g. `title="Незначителна облачност"`) that nothing was reading. Now
captured in `src/meteo/scrapers/dalivali.py`.

**c) freemeteo.bg redesigned its "15-days" page.** The forecast section
the original scraper targeted (`fifteen-day-forecast`) is now a Recharts
SVG line chart that only exposes date + max temp — no min temp, wind,
rain, or description at all, for anyone. The actual per-day detail moved
to a different section entirely (a day-selector strip linking to
`hourly-forecast/dayN`). Rewrote `src/meteo/scrapers/freemeteo.py`
end-to-end against that new structure. Two quirks worth remembering if
this breaks again:
  - That strip also contains decoy nav links ("Почасово" tab buttons)
    that share the same `/today/`-ish href as the real "today" card but
    carry no forecast data — cards are identified by "has a
    `img[data-forecast-code]` icon", not by href pattern.
  - Tomorrow's card is labeled `"Утре"` instead of a date (today's would
    be `"Днес"`, but today is always skipped) — every other day has a
    real `"DD MM"` date. This is the same quirk v1 had for the old page
    layout, just needed re-discovering on the new one.
  - The scraper forces a wide browser window (`1400x1000`) specifically
    so only the desktop CSS layout renders — the page keeps both a mobile
    and desktop copy of every day's markup in the DOM at once, and
    `.innerText` only reflects the visible one. If this scraper ever
    starts returning wrong/missing fields again, check whether the
    window-size trick is still forcing the right layout first.

## 4. Current verified status

All 9 combinations (3 cities × 3 sources) run end-to-end and write real
rows to Postgres — verified live, not just unit tests. Unit tests
(`pytest`, 21 tests) also pass.

## 5. Commit history on `v2`

All fixes from section 3, plus this doc, are committed locally on `v2` as
of commit `359979a`:
```
359979a Fix local driver setup and real DB/scraping bugs found in live testing
7578017 Comment out scheduled cron job in GitHub Actions workflow
f3d0699 Add hourly GitHub Actions workflow to run the scraper
e02ad55 Rewrite project as installable package (v2)
```
**Nothing has been pushed to `origin` (GitHub) yet** — everything above is
local-only. `main` is untouched throughout.

Re-verified after committing `359979a`: `pytest` (21/21 passing) and a
full `python main.py --city sofia` run (all 3 sources) both still succeed
against live Postgres — the commit didn't introduce any regression.

## 6. Loose ends worth knowing about, not yet addressed

- **`Dalivali.humidity` and `Freemeteo.rain` type coercion**: both are
  scraped as plain strings and rely on Postgres implicitly coercing
  unquoted-literal parameters to the target column's actual type
  (`humidity` is `integer`, `rain` is `text`) at insert time. This works
  today but is a bit implicit — if a future site change makes either
  field contain something non-numeric where the DB expects a number,
  you'll get a runtime insert error, not a caught validation error.
- **`Image.name` uniqueness was never confirmed.** `docs/image-capture.md`
  flags this: if you ever implement real image capture, verify there's
  actually a unique constraint on `Image.name` before relying on
  `ON CONFLICT (name)`.
- **freemeteo's new scraper is inherently more fragile than before**,
  since it now depends on a CSS-breakpoint trick (window size) rather
  than just element selectors. Worth an occasional `--no-headless` sanity
  check after freemeteo.bg does another redesign.
