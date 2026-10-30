"""Middleware base class."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..context import Context

Handler = Callable[..., Awaitable[Any]]


class BaseMiddleware(ABC):
    @abstractmethod
    async def __call__(
        self,
        handler: Handler,
        ctx: Context,
        data: dict[str, Any],
    ) -> Any:
        ...
