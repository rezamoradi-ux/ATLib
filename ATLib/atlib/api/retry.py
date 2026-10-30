"""Retry policy with exponential backoff and jitter."""

from __future__ import annotations
import asyncio
import random
from typing import Callable, Awaitable, TypeVar
from ..exceptions import RateLimitError, NetworkError, TimeoutError, TelegramAPIError

T = TypeVar("T")


class RetryPolicy:
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 0.5,
        max_delay: float = 30.0,
        jitter: float = 0.2,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter

    def should_retry(self, exc: Exception, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False
        if isinstance(exc, RateLimitError):
            return True
        if isinstance(exc, (NetworkError, TimeoutError)):
            return True
        if isinstance(exc, TelegramAPIError) and exc.error_code in (429, 500, 502, 503, 504):
            return True
        return False

    def delay_for(self, attempt: int, retry_after: float | None = None) -> float:
        if retry_after is not None:
            return float(retry_after)
        delay = min(self.max_delay, self.base_delay * (2 ** attempt))
        jitter = delay * self.jitter * random.random()
        return delay + jitter

    async def run(self, coro_factory: Callable[[], Awaitable[T]]) -> T:
        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await coro_factory()
            except Exception as exc:
                last_exc = exc
                if not self.should_retry(exc, attempt):
                    raise
                retry_after = getattr(exc, "retry_after", None)
                delay = self.delay_for(attempt, retry_after)
                await asyncio.sleep(delay)
        assert last_exc is not None
        raise last_exc
