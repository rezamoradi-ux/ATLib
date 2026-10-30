"""Storage interface for FSM and other persistent data."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    @abstractmethod
    async def get_state(self, key: str) -> str | None:
        ...

    @abstractmethod
    async def set_state(self, key: str, state: str | None) -> None:
        ...

    @abstractmethod
    async def get_data(self, key: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def set_data(self, key: str, data: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def update_data(self, key: str, data: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def clear(self, key: str) -> None:
        ...

    async def close(self) -> None:
        pass
