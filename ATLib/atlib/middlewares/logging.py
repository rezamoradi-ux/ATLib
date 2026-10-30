"""Request logging middleware."""

from __future__ import annotations
import time
from typing import Any, Callable, Awaitable
from ..logging import get_logger
from .base import BaseMiddleware

log = get_logger("middleware.logging")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        ctx: Any,
        data: dict[str, Any],
    ) -> Any:
        start = time.monotonic()
        update_id = ctx.update.update_id
        log.info("Processing update %s", update_id)
        try:
            result = await handler(ctx)
            elapsed = (time.monotonic() - start) * 1000
            log.info("Update %s handled in %.1fms", update_id, elapsed)
            return result
        except Exception:
            elapsed = (time.monotonic() - start) * 1000
            log.exception("Update %s failed after %.1fms", update_id, elapsed)
            raise
