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
  **default branch** (`main`). This used to block cron entirely (see
  section 5) — it's resolved now that `v2` has been merged into `main`.

### Where the workflow's parameters actually come from

Nothing about *what* the workflow scrapes is configurable from the
workflow file itself — it just runs `python main.py` with no CLI flags,
so every default baked into the code applies:

| Parameter | Value when the workflow runs | Where it's actually set |
|---|---|---|
| Cities scraped | All 3 (Plovdiv, Sofia, Vidin) | `src/meteo/config.py` — the `CITIES` registry. No `--city` flag is passed, so `cli.py` defaults to all of them. |
| Sources scraped | All 3 (freemeteo, dalivali, sinoptik) | Same file, `SOURCES` tuple. No `--source` flag passed. |
| Headless mode | Always headless (no visible browser — there's no display on a CI runner anyway) | CLI default in `src/meteo/cli.py` (`--no-headless` not passed) |
| Log level | `INFO` | CLI default in `src/meteo/cli.py` |
| Python version | 3.12 | Set directly in the workflow file, `actions/setup-python@v5` step |
| Runner OS | `ubuntu-latest` | Set directly in the workflow file (`runs-on:`) — this is what gives it Firefox + geckodriver preinstalled |
| Python dependencies | Whatever `pyproject.toml` lists (`selenium`, `psycopg2-binary`, `python-dotenv`) | `pip install -e .` reads `pyproject.toml` directly; `webdriver-manager` is commented out there, unused |
| DB connection (`PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGSSLMODE`) | Whatever's configured on GitHub | **GitHub repo → Settings → Secrets and variables → Actions → Repository secrets.** Not visible in any file — that's the point of using secrets. Injected into the job as env vars in the workflow file's `env:` block, then read via `os.getenv(...)` in `src/meteo/settings.py`. |

To scrape a subset instead (e.g. only Sofia, or only one source), the
workflow file's `- run: python main.py` line would need arguments added,
e.g. `python main.py --city sofia --source sinoptik` — nothing like that
exists today; every run does the full 3×3 sweep.

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

## 5. Commit history, and `v2` → `main`

All fixes from section 3, plus this doc, were committed locally on `v2`:
```
359979a Fix local driver setup and real DB/scraping bugs found in live testing
7578017 Comment out scheduled cron job in GitHub Actions workflow
f3d0699 Add hourly GitHub Actions workflow to run the scraper
e02ad55 Rewrite project as installable package (v2)
```

At the time those were written, this doc said "nothing has been pushed to
`origin` yet." **That went stale without this session doing it.** At some
point outside this session, `v2` was pushed to GitHub and merged into
`main` via PR #2 (`13e3a26 Merge pull request #2 from Simeonov98/v2`, plus
an intermediate `b860c74 update docs` on `v2` after the commits above).
This session only noticed because a later `git status` reported "ahead of
origin/v2" unexpectedly. Current state, confirmed directly:
- `main` (local) is in sync with `origin/main`, at `13e3a26` — this is the
  full v2 rewrite, merged.
- `v2` (local and `origin/v2`) is also in sync, at `b860c74`.
- So: **v2 is live on the default branch.** This is what resolves the
  "cron won't fire" caveat in section 2 above.

Re-verified after committing `359979a` (before the merge existed):
`pytest` (21/21 passing) and a full `python main.py --city sofia` run (all
3 sources) both still succeeded against live Postgres — that commit didn't
introduce any regression.

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
