"""Callback data filters."""

from __future__ import annotations
import re
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class CallbackData(Filter):
    def __init__(self, data: str | None = None, *, prefix: str | None = None, regex: str | None = None):
        self.data = data
        self.prefix = prefix
        self.pattern = re.compile(regex) if regex else None

    async def check(self, update: Update, ctx: Context) -> bool:
        cq = update.callback_query
        if not cq or cq.data is None:
            return False
        if self.data is not None:
            return cq.data == self.data
        if self.prefix is not None:
            return cq.data.startswith(self.prefix)
        if self.pattern is not None:
            return bool(self.pattern.match(cq.data))
        return True
