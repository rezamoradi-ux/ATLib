"""User filters."""

from __future__ import annotations
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class UserId(Filter):
    def __init__(self, *user_ids: int):
        self.ids = set(user_ids)

    async def check(self, update: Update, ctx: Context) -> bool:
        user = update.effective_user
        return bool(user and user.id in self.ids)


class Username(Filter):
    def __init__(self, *usernames: str):
        self.names = {u.lstrip("@").lower() for u in usernames}

    async def check(self, update: Update, ctx: Context) -> bool:
        user = update.effective_user
        return bool(user and user.username and user.username.lower() in self.names)
