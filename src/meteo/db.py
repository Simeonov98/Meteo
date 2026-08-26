"""Postgres access layer. Single source of truth for the DB connection and
the only place that knows the forecast table schemas.

All inserts are parameterized (no f-string SQL) so scraped text containing
quotes or special characters can't corrupt a query.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterable, Iterator

import psycopg2
from psycopg2 import pool as pg_pool

from meteo.models import DalivaliForecast, FreemeteoForecast, SinoptikForecast
from meteo.settings import get_settings

logger = logging.getLogger(__name__)

_pool: pg_pool.SimpleConnectionPool | None = None


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


def insert_freemeteo(rows: Iterable[FreemeteoForecast]) -> int:
    query = """
        INSERT INTO "Freemeteo" ("forecastDay", weekday, tmax, tmin, text, wdir, rain, "cityId", "imageId")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [
        (r.forecast_day, r.weekday, r.tmax, r.tmin, r.text, r.wdir, r.rain, r.city_id, r.image_id)
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
        (r.forecast_day, r.weekday, r.tmax, r.tmin, r.wspd, r.wdir, r.humidity, r.text, r.city_id, r.image_id)
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
        (r.forecast_date, r.weekday, r.tmax, r.tmin, r.wdir, r.wspd, r.text, r.city_id, r.image_id)
        for r in rows
    ]
    with cursor() as cur:
        cur.executemany(query, params)
    logger.info("inserted %d Sinoptik rows", len(params))
    return len(params)
