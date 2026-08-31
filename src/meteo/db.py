"""Postgres access layer. Single source of truth for the DB connection and
the only place that knows the forecast table schemas.

All inserts are parameterized (no f-string SQL) so scraped text containing
quotes or special characters can't corrupt a query.
"""

from __future__ import annotations

import base64
import logging
from contextlib import contextmanager
from typing import Iterable, Iterator

import psycopg2
from psycopg2 import pool as pg_pool

from meteo.models import NO_IMAGE_ID, DalivaliForecast, FreemeteoForecast, SinoptikForecast
from meteo.settings import get_settings

logger = logging.getLogger(__name__)

_pool: pg_pool.SimpleConnectionPool | None = None

# "imageId" turned out to have a real foreign key against "Image" in
# production (image_fk / sinoptik_imageid_fk), unlike what local schema
# introspection against a different database showed -- NO_IMAGE_ID=0 alone
# isn't a valid reference. Get-or-create one placeholder Image row instead,
# and point every forecast without a real per-day screenshot at it. See
# docs/image-capture.md for the real-image-capture path this stands in for.
_PLACEHOLDER_IMAGE_NAME = "no-image"
_PLACEHOLDER_IMAGE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)
_placeholder_image_id: int | None = None


def _get_pool() -> pg_pool.SimpleConnectionPool:
    global _pool
    if _pool is None:
        s = get_settings()
        _pool = pg_pool.SimpleConnectionPool(
            1,
            5,
            host=s.pg_host,
            dbname=s.pg_database,
            user=s.pg_user,
            password=s.pg_password,
            sslmode=s.pg_sslmode,
        )
    return _pool


@contextmanager
def cursor() -> Iterator[psycopg2.extensions.cursor]:
    conn = _get_pool().getconn()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _get_pool().putconn(conn)


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None


def _get_placeholder_image_id() -> int:
    global _placeholder_image_id
    if _placeholder_image_id is not None:
        return _placeholder_image_id
    with cursor() as cur:
        cur.execute('SELECT id FROM "Image" WHERE name = %s', (_PLACEHOLDER_IMAGE_NAME,))
        row = cur.fetchone()
        if row is None:
            cur.execute(
                'INSERT INTO "Image" (name, src) VALUES (%s, %s) RETURNING id',
                (_PLACEHOLDER_IMAGE_NAME, _PLACEHOLDER_IMAGE_PNG),
            )
            row = cur.fetchone()
    _placeholder_image_id = row[0]
    return _placeholder_image_id


def _resolve_image_id(image_id: int) -> int:
    return _get_placeholder_image_id() if image_id == NO_IMAGE_ID else image_id


def insert_freemeteo(rows: Iterable[FreemeteoForecast]) -> int:
    query = """
        INSERT INTO "Freemeteo" ("forecastDay", weekday, tmax, tmin, text, wdir, rain, "cityId", "imageId")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [
        (r.forecast_day, r.weekday, r.tmax, r.tmin, r.text, r.wdir, r.rain, r.city_id, _resolve_image_id(r.image_id))
        for r in rows
    ]
    with cursor() as cur:
        cur.executemany(query, params)
    logger.info("inserted %d Freemeteo rows", len(params))
    return len(params)


def insert_dalivali(rows: Iterable[DalivaliForecast]) -> int:
    query = """
        INSERT INTO "Dalivali" ("forecastDay", weekday, tmax, tmin, wspd, wdir, humidity, text, "cityId", "imageId")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [
        (
            r.forecast_day,
            r.weekday,
            r.tmax,
            r.tmin,
            r.wspd,
            r.wdir,
            r.humidity,
            r.text,
            r.city_id,
            _resolve_image_id(r.image_id),
        )
        for r in rows
    ]
    with cursor() as cur:
        cur.executemany(query, params)
    logger.info("inserted %d Dalivali rows", len(params))
    return len(params)


def insert_sinoptik(rows: Iterable[SinoptikForecast]) -> int:
    query = """
        INSERT INTO "Sinoptik" ("forecastDate", weekday, tmax, tmin, wdir, wspd, text, "cityId", "imageId")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [
        (r.forecast_date, r.weekday, r.tmax, r.tmin, r.wdir, r.wspd, r.text, r.city_id, _resolve_image_id(r.image_id))
        for r in rows
    ]
    with cursor() as cur:
        cur.executemany(query, params)
    logger.info("inserted %d Sinoptik rows", len(params))
    return len(params)
