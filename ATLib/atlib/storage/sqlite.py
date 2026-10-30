"""Async-safe SQLite storage using aiosqlite if available, else stdlib with lock."""

from __future__ import annotations
import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Any
from .base import BaseStorage
from ..exceptions import StorageError


class SQLiteStorage(BaseStorage):
    def __init__(self, path: str | Path = "atlib_fsm.db"):
        self.path = str(path)
        self._lock = asyncio.Lock()
        self._conn: sqlite3.Connection | None = None
        self._init_done = False

    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    async def _ensure_schema(self) -> None:
        if self._init_done:
            return
        async with self._lock:
            if self._init_done:
                return
            conn = self._connect()
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fsm (
                    key TEXT PRIMARY KEY,
                    state TEXT,
                    data TEXT NOT NULL DEFAULT '{}'
                )
                """
            )
            conn.commit()
            self._init_done = True

    async def get_state(self, key: str) -> str | None:
        await self._ensure_schema()
        async with self._lock:
            row = self._connect().execute(
                "SELECT state FROM fsm WHERE key = ?", (key,)
            ).fetchone()
            return row["state"] if row else None

    async def set_state(self, key: str, state: str | None) -> None:
        await self._ensure_schema()
        async with self._lock:
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO fsm (key, state, data) VALUES (?, ?, '{}')
                ON CONFLICT(key) DO UPDATE SET state = excluded.state
                """,
                (key, state),
            )
            conn.commit()

    async def get_data(self, key: str) -> dict[str, Any]:
        await self._ensure_schema()
        async with self._lock:
            row = self._connect().execute(
                "SELECT data FROM fsm WHERE key = ?", (key,)
            ).fetchone()
            if not row:
                return {}
            return json.loads(row["data"])

    async def set_data(self, key: str, data: dict[str, Any]) -> None:
        await self._ensure_schema()
        async with self._lock:
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO fsm (key, state, data) VALUES (?, NULL, ?)
                ON CONFLICT(key) DO UPDATE SET data = excluded.data
                """,
                (key, json.dumps(data)),
            )
            conn.commit()

    async def update_data(self, key: str, data: dict[str, Any]) -> dict[str, Any]:
        current = await self.get_data(key)
        current.update(data)
        await self.set_data(key, current)
        return current

    async def clear(self, key: str) -> None:
        await self._ensure_schema()
        async with self._lock:
            conn = self._connect()
            conn.execute("DELETE FROM fsm WHERE key = ?", (key,))
            conn.commit()

    async def close(self) -> None:
        async with self._lock:
            if self._conn is not None:
                self._conn.close()
                self._conn = None
