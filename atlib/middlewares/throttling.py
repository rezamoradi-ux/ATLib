"""Simple anti-flood / throttling middleware."""

from __future__ import annotations
import time
from typing import Any, Callable, Awaitable
from collections import defaultdict
from .base import BaseMiddleware


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self._last: dict[int, float] = defaultdict(float)

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        ctx: Any,
        data: dict[str, Any],
    ) -> Any:
        user = ctx.user
        if user is None:
            return await handler(ctx)
        now = time.monotonic()
        last = self._last[user.id]
        if now - last < self.rate_limit:
            return None  # drop
        self._last[user.id] = now
        return await handler(ctx)
