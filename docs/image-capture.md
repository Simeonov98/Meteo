# Per-forecast image capture — history and how to bring it back

## What v1 tried to do

Every insert into `Freemeteo`, `Dalivali`, and `Sinoptik` has a NOT NULL
`imageId` column, meant to point at a row in a separate `Image` table
(`id`, `name` text, `src` bytea) holding a screenshot of that day's weather
icon.

The intended flow, as built in `archive/db2.py` (`insertBLOB`) and the old
`sinoptik.py`:

1. Screenshot the day's icon element with Selenium (`element.screenshot(path)`).
2. MD5-hash the file (`archive/hash.py: getHash`) and rename it to
   `<hash>.png` — this doubles as content-based dedup: identical icons
   (e.g. "clear sky" reused across many days) hash to the same filename.
3. Insert `(name=hash, src=file bytes)` into `Image`, `ON CONFLICT (name)
   DO NOTHING` (skip if that exact icon was already stored).
4. Insert the forecast row with `imageId = (SELECT id FROM "Image" WHERE
   name = '<hash>')`.

## Why it never actually worked

Step 3 was commented out in every scraper (`# for img in imageDbStr: #
db2.insertBLOB(...)`). So step 4's subquery always matched zero rows and
`imageId` evaluated to `NULL` — violating the NOT NULL constraint on every
single insert, silently, because `archive/db3.py: push()` swallowed all
exceptions with a bare `print()` instead of raising. This almost certainly
means **no forecast row was ever successfully written by v1**, for any
source, for as long as `imageId` has been NOT NULL — not something this
rewrite broke.

There was also a standing bug in step 1/2: the screenshot was written to a
hardcoded path (`/home/simeon/programming/Meteo/sinoptik/...`), which only
existed on the original author's Linux machine.

## Where v2 stands

v2 doesn't capture images at all. `imageId` is filled with a sentinel
constant, `NO_IMAGE_ID = 0` (`src/meteo/models.py`), which is safe because
**there is no foreign key on `imageId`** (confirmed via
`information_schema` — it's a plain NOT NULL integer, nothing enforces it
points at a real `Image` row).

## How to properly re-implement it, if you want it back

1. **Capture in-memory, not to disk.** Selenium's
   `element.screenshot_as_png` returns raw PNG bytes directly — no temp
   file, no rename dance, no hardcoded path:
   ```python
   png_bytes = icon_element.screenshot_as_png
   ```
   Per-source icon elements already identified in the current scrapers:
   - freemeteo: `img[data-forecast-code]`
   - dalivali: `.icon-forecast img`
   - sinoptik: `.wf10dayRightImg`

2. **Hash the bytes directly** for content-based dedup:
   ```python
   image_name = hashlib.md5(png_bytes).hexdigest()
   ```

3. **Get-or-create the `Image` row**, since `INSERT ... ON CONFLICT (name)
   DO NOTHING` doesn't return an id on the conflict path — you need a
   real get-or-create, e.g. in `src/meteo/db.py`:
   ```python
   def get_or_create_image(name: str, src: bytes) -> int:
       with cursor() as cur:
           cur.execute('SELECT id FROM "Image" WHERE name = %s', (name,))
           row = cur.fetchone()
           if row:
               return row[0]
           cur.execute(
               'INSERT INTO "Image" (name, src) VALUES (%s, %s) RETURNING id',
               (name, src),
           )
           return cur.fetchone()[0]
   ```
   (Confirm whether `Image.name` actually has a unique constraint before
   relying on `ON CONFLICT (name)` — the schema introspection that found
   the NOT NULL columns didn't check this.)

4. **Wire the returned id into `image_id`** on the relevant dataclass
   (`FreemeteoForecast` / `DalivaliForecast` / `SinoptikForecast`) before
   calling `db.insert_*`. This has to happen inside each scraper's parsing
   loop, since it needs a live `WebElement` handle to screenshot — it
   can't live in `db.py` alone.

5. **Decide if this is worth the cost before doing it**: it roughly
   doubles the number of Selenium calls per day parsed (one extra
   round-trip per icon) and adds a DB round-trip per row. Worth checking
   first whether anything downstream (the NextJS frontend mentioned in the
   original README, if it still exists) actually renders these images —
   if nothing reads `Image`, this is pure cost with no payoff.
