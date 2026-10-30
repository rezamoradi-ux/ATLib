"""Per-user/chat FSM context."""

from __future__ import annotations
from typing import Any
from ..storage.base import BaseStorage


class FSMContext:
    def __init__(self, storage: BaseStorage, key: str):
        self.storage = storage
        self.key = key

    async def get_state(self) -> str | None:
        return await self.storage.get_state(self.key)

    async def set_state(self, state: Any) -> None:
        value = str(state) if state is not None else None
        await self.storage.set_state(self.key, value)

    async def get_data(self) -> dict[str, Any]:
        return await self.storage.get_data(self.key)

    async def set_data(self, data: dict[str, Any]) -> None:
        await self.storage.set_data(self.key, data)

    async def update_data(self, **kwargs: Any) -> dict[str, Any]:
        return await self.storage.update_data(self.key, kwargs)

    async def clear(self) -> None:
        await self.storage.clear(self.key)
