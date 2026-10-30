"""Text filters."""

from __future__ import annotations
import re
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class Text(Filter):
    """Matches any non-empty text message."""

    async def check(self, update: Update, ctx: Context) -> bool:
        msg = update.effective_message
        return bool(msg and msg.text)


class ExactText(Filter):
    def __init__(self, text: str, *, ignore_case: bool = False):
        self.text = text
        self.ignore_case = ignore_case

    async def check(self, update: Update, ctx: Context) -> bool:
        msg = update.effective_message
        if not msg or msg.text is None:
            return False
        if self.ignore_case:
            return msg.text.lower() == self.text.lower()
        return msg.text == self.text


class Regex(Filter):
    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = re.compile(pattern, flags)

    async def check(self, update: Update, ctx: Context) -> bool:
        msg = update.effective_message
        if not msg or not msg.text:
            return False
        return bool(self.pattern.search(msg.text))
