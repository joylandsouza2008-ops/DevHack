"""
The database for "My ponds and devices" (backend/ponds.py).

Where the data lives, decided once when the server starts (open_from_env):
    DATABASE_URL is set (Render Postgres)  -> Postgres. Ponds survive restarts.
    running on Render without DATABASE_URL -> memory only ("demo mode": ponds reset
                                              when the free server sleeps).
    on your own computer                   -> a SQLite file, data/aquanexus.db
                                              (data/ is not in git).

The rest of the app only uses Database.execute / query / one, with "?" in the
SQL for values. Postgres wants "%s" instead; that is swapped here, so the same
plain SQL works on both. Values are always passed separately, never pasted into
the SQL text, so a pond name can't change the SQL (no SQL injection).
"""

from __future__ import annotations

import logging
import os
import sqlite3
import threading
from pathlib import Path

log = logging.getLogger("uvicorn.error")
SQLITE_FILE = Path(__file__).resolve().parent.parent / "data" / "aquanexus.db"

SCHEMA = [
    # A farm is a group of ponds. Its id is a hash of the farm code: the code itself is never stored.
    "CREATE TABLE IF NOT EXISTS farms (id TEXT PRIMARY KEY, created_at TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS ponds (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL, name TEXT NOT NULL, "
    "size TEXT, fish TEXT, created_at TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS ponds_farm ON ponds (farm_id)",
    # One device per pond. Only a hash of its key is kept.
    "CREATE TABLE IF NOT EXISTS devices (id TEXT PRIMARY KEY, pond_id TEXT NOT NULL UNIQUE, "
    "key_hash TEXT NOT NULL, created_at TEXT NOT NULL, last_seen TEXT, last_try TEXT, last_error TEXT)",
    # Readings: the values as JSON text, plus the level so the latest status is cheap to read.
    "CREATE TABLE IF NOT EXISTS readings (pond_id TEXT NOT NULL, device_id TEXT NOT NULL, "
    "received_at TEXT NOT NULL, measured_at TEXT NOT NULL, level TEXT NOT NULL, demo INTEGER NOT NULL, "
    "data_json TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS readings_pond_time ON readings (pond_id, received_at)",
    # Warning and Danger alerts, one row each time a pond's level or cause changes.
    "CREATE TABLE IF NOT EXISTS alerts (pond_id TEXT NOT NULL, farm_id TEXT NOT NULL, time TEXT NOT NULL, "
    "level TEXT NOT NULL, causes TEXT NOT NULL, summary_json TEXT NOT NULL, demo INTEGER NOT NULL)",
    "CREATE INDEX IF NOT EXISTS alerts_farm_time ON alerts (farm_id, time)",
]


class Database:
    """One connection, shared by all requests, with a lock (the app is small)."""

    def __init__(self, kind: str, connection, placeholder: str = "?", reopen=None) -> None:
        self.kind = kind                     # "postgres", "sqlite" or "memory"
        self._conn = connection
        self._reopen = reopen                # Postgres: makes a new connection if the old one dropped
        self._placeholder = placeholder
        self._lock = threading.Lock()
        for statement in SCHEMA:
            self.execute(statement)

    @property
    def persistent(self) -> bool:
        """False in demo mode: everything is lost when the server restarts."""
        return self.kind != "memory"

    def _sql(self, sql: str) -> str:
        return sql if self._placeholder == "?" else sql.replace("?", self._placeholder)

    def _run(self, sql: str, params: tuple, fetch: bool):
        with self._lock:
            if self._reopen and getattr(self._conn, "closed", False):
                self._conn = self._reopen()
            try:
                cur = self._conn.cursor()
                cur.execute(self._sql(sql), params)
                if fetch:
                    names = [c[0] for c in cur.description]
                    return [dict(zip(names, row)) for row in cur.fetchall()]
                self._conn.commit()
                return None
            except Exception:
                try:
                    self._conn.rollback()        # a failed statement must not block the next one
                except Exception:
                    pass
                raise

    def execute(self, sql: str, params: tuple = ()) -> None:
        self._run(sql, params, fetch=False)

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        return self._run(sql, params, fetch=True)

    def one(self, sql: str, params: tuple = ()) -> dict | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None


def memory() -> Database:
    return Database("memory", sqlite3.connect(":memory:", check_same_thread=False))


def sqlite_file(path: Path = SQLITE_FILE) -> Database:
    path.parent.mkdir(parents=True, exist_ok=True)
    return Database("sqlite", sqlite3.connect(path, check_same_thread=False))


def postgres(url: str) -> Database:
    import psycopg                              # only needed when DATABASE_URL is set
    connect = lambda: psycopg.connect(url, autocommit=True)
    return Database("postgres", connect(), placeholder="%s", reopen=connect)


def open_from_env() -> Database:
    """Postgres if DATABASE_URL is set, memory on Render without it, else a local SQLite file."""
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        try:
            return postgres(url)
        except Exception as error:              # wrong URL, database asleep, driver missing ...
            log.error("DATABASE_URL is set but the database could not be opened (%s). "
                      "Using memory: ponds reset when the server sleeps.", type(error).__name__)
            return memory()
    if os.environ.get("RENDER"):                # Render sets this; its disk is wiped on every restart
        return memory()
    return sqlite_file(Path(os.environ.get("SQLITE_PATH", SQLITE_FILE)))
