"""FSM manager that creates contexts for updates."""

from __future__ import annotations
from typing import Any
from ..storage.base import BaseStorage
from ..types.updates import Update
from .context import FSMContext


class FSMManager:
    def __init__(self, storage: BaseStorage, *, strategy: str = "user"):
        """
        strategy:
          - "user": key = user_id
          - "chat": key = chat_id
          - "chat_user": key = chat_id:user_id
        """
        self.storage = storage
        self.strategy = strategy

    def resolve_key(self, update: Update) -> str:
        user = update.effective_user
        chat = update.effective_chat
        if self.strategy == "chat":
            return f"chat:{chat.id}" if chat else "chat:unknown"
        if self.strategy == "chat_user":
            uid = user.id if user else 0
            cid = chat.id if chat else 0
            return f"chat_user:{cid}:{uid}"
        # default user
        return f"user:{user.id}" if user else "user:unknown"

    async def get_context(self, update: Update) -> FSMContext:
        key = self.resolve_key(update)
        return FSMContext(self.storage, key)
