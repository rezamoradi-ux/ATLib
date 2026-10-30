"""Composable filter base classes."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class Filter(ABC):
    @abstractmethod
    async def check(self, update: Update, ctx: Context) -> bool:
        ...

    def __and__(self, other: Filter) -> AndFilter:
        return AndFilter(self, other)

    def __or__(self, other: Filter) -> OrFilter:
        return OrFilter(self, other)

    def __invert__(self) -> NotFilter:
        return NotFilter(self)


class AndFilter(Filter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, update: Update, ctx: Context) -> bool:
        for f in self.filters:
            if not await f.check(update, ctx):
                return False
        return True


class OrFilter(Filter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, update: Update, ctx: Context) -> bool:
        for f in self.filters:
            if await f.check(update, ctx):
                return True
        return False


class NotFilter(Filter):
    def __init__(self, filter_: Filter):
        self.filter = filter_

    async def check(self, update: Update, ctx: Context) -> bool:
        return not await self.filter.check(update, ctx)
