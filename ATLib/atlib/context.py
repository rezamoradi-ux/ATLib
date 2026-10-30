"""Handler execution context."""

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .types.updates import Update
from .types.messages import Message
from .types.callbacks import CallbackQuery
from .types.users import User
from .types.chats import Chat

if TYPE_CHECKING:
    from .bot import Bot
    from .fsm.context import FSMContext


class Context:
    """Per-update context passed to handlers."""

    def __init__(
        self,
        bot: Bot,
        update: Update,
        *,
        data: dict[str, Any] | None = None,
        fsm: FSMContext | None = None,
    ):
        self.bot = bot
        self.update = update
        self.data = data or {}
        self.fsm = fsm

    @property
    def message(self) -> Message | None:
        return self.update.effective_message

    @property
    def callback_query(self) -> CallbackQuery | None:
        return self.update.callback_query

    @property
    def user(self) -> User | None:
        return self.update.effective_user

    @property
    def chat(self) -> Chat | None:
        return self.update.effective_chat

    async def answer(self, text: str, **kwargs: Any) -> Message:
        if not self.chat:
            raise RuntimeError("No chat to answer to")
        return await self.bot.send_message(self.chat.id, text, **kwargs)

    async def reply(self, text: str, **kwargs: Any) -> Message:
        if not self.message:
            raise RuntimeError("No message to reply to")
        return await self.bot.send_message(
            self.message.chat.id,
            text,
            reply_parameters={"message_id": self.message.message_id},
            **kwargs,
        )
