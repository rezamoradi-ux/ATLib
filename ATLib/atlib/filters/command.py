"""Command filter."""

from __future__ import annotations
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class Command(Filter):
    def __init__(self, *commands: str, prefixes: str = "/"):
        self.commands = {c.lower().lstrip("/") for c in commands}
        self.prefixes = prefixes

    async def check(self, update: Update, ctx: Context) -> bool:
        msg = update.effective_message
        if not msg or not msg.text:
            return False
        text = msg.text.strip()
        if not text or text[0] not in self.prefixes:
            return False
        parts = text[1:].split(maxsplit=1)
        cmd = parts[0].split("@")[0].lower()
        return cmd in self.commands
