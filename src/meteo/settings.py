"""Environment-backed settings.

Note: the old db3.py read HOST/DATABASE/DB_USERNAME/PASSWORD/SSL_CERT, but
the actual .env file (and every deployment of it) uses the standard libpq
names PGHOST/PGDATABASE/PGUSER/PGPASSWORD/PGSSLMODE. Those old lookups
always returned None -- it only worked because passing host=None etc. to
psycopg2 makes libpq fall back to reading PGHOST/PGDATABASE/... straight out
of the process environment. This module reads the real variable names
explicitly instead of relying on that fallback.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    pg_host: str | None
    pg_database: str | None
    pg_user: str | None
    pg_password: str | None
    pg_sslmode: str | None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        pg_host=os.getenv("PGHOST"),
        pg_database=os.getenv("PGDATABASE"),
        pg_user=os.getenv("PGUSER"),
        pg_password=os.getenv("PGPASSWORD"),
        pg_sslmode=os.getenv("PGSSLMODE", "require"),
    )
