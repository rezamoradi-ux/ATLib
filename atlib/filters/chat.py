"""Chat type filters."""

from __future__ import annotations
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class Private(Filter):
    async def check(self, update: Update, ctx: Context) -> bool:
        chat = update.effective_chat
        return bool(chat and chat.type == "private")


class Group(Filter):
    async def check(self, update: Update, ctx: Context) -> bool:
        chat = update.effective_chat
        return bool(chat and chat.type in ("group", "supergroup"))


class Supergroup(Filter):
    async def check(self, update: Update, ctx: Context) -> bool:
        chat = update.effective_chat
        return bool(chat and chat.type == "supergroup")


class Channel(Filter):
    async def check(self, update: Update, ctx: Context) -> bool:
        chat = update.effective_chat
        return bool(chat and chat.type == "channel")
