"""Simple token-bucket rate limiter."""

from __future__ import annotations
import asyncio
import time


class RateLimiter:
    def __init__(self, rate: float = 25.0, capacity: float | None = None):
        self.rate = rate
        self.capacity = capacity or rate
        self.tokens = self.capacity
        self.updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.updated = now
            if self.tokens < tokens:
                wait = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait)
                self.tokens = 0
                self.updated = time.monotonic()
            else:
                self.tokens -= tokens
