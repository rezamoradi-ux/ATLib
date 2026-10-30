"""In-memory storage (not durable across restarts)."""

from __future__ import annotations
from typing import Any
from .base import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self) -> None:
        self._states: dict[str, str | None] = {}
        self._data: dict[str, dict[str, Any]] = {}

    async def get_state(self, key: str) -> str | None:
        return self._states.get(key)

    async def set_state(self, key: str, state: str | None) -> None:
        if state is None:
            self._states.pop(key, None)
        else:
            self._states[key] = state

    async def get_data(self, key: str) -> dict[str, Any]:
        return dict(self._data.get(key, {}))

    async def set_data(self, key: str, data: dict[str, Any]) -> None:
        self._data[key] = dict(data)

    async def update_data(self, key: str, data: dict[str, Any]) -> dict[str, Any]:
        current = self._data.setdefault(key, {})
        current.update(data)
        return dict(current)

    async def clear(self, key: str) -> None:
        self._states.pop(key, None)
        self._data.pop(key, None)
