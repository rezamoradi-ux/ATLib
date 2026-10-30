"""Catch and log handler exceptions."""

from __future__ import annotations
from typing import Any, Callable, Awaitable
from ..logging import get_logger
from .base import BaseMiddleware

log = get_logger("middleware.error")


class ErrorHandlingMiddleware(BaseMiddleware):
    def __init__(self, *, reraise: bool = True):
        self.reraise = reraise

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        ctx: Any,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(ctx)
        except Exception as exc:
            log.exception("Unhandled error in handler: %s", exc)
            if self.reraise:
                raise
            return None
