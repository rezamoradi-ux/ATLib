"""Callback query types."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .users import User
from .messages import Message


@dataclass
class CallbackQuery:
    id: str
    from_user: User
    chat_instance: str
    message: Message | None = None
    inline_message_id: str | None = None
    data: str | None = None
    game_short_name: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CallbackQuery | None:
        if not data:
            return None
        return cls(
            id=data["id"],
            from_user=User.from_dict(data["from"]) or User(id=0, is_bot=False, first_name=""),
            chat_instance=data.get("chat_instance", ""),
            message=Message.from_dict(data.get("message")),
            inline_message_id=data.get("inline_message_id"),
            data=data.get("data"),
            game_short_name=data.get("game_short_name"),
            raw=data,
        )
