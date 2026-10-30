"""Update type covering all documented update fields."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .messages import Message
from .callbacks import CallbackQuery
from .users import User
from .chats import Chat


@dataclass
class Update:
    update_id: int
    message: Message | None = None
    edited_message: Message | None = None
    channel_post: Message | None = None
    edited_channel_post: Message | None = None
    callback_query: CallbackQuery | None = None
    inline_query: dict[str, Any] | None = None
    chosen_inline_result: dict[str, Any] | None = None
    shipping_query: dict[str, Any] | None = None
    pre_checkout_query: dict[str, Any] | None = None
    poll: dict[str, Any] | None = None
    poll_answer: dict[str, Any] | None = None
    my_chat_member: dict[str, Any] | None = None
    chat_member: dict[str, Any] | None = None
    chat_join_request: dict[str, Any] | None = None
    business_connection: dict[str, Any] | None = None
    business_message: Message | None = None
    message_reaction: dict[str, Any] | None = None
    message_reaction_count: dict[str, Any] | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Update:
        return cls(
            update_id=data["update_id"],
            message=Message.from_dict(data.get("message")),
            edited_message=Message.from_dict(data.get("edited_message")),
            channel_post=Message.from_dict(data.get("channel_post")),
            edited_channel_post=Message.from_dict(data.get("edited_channel_post")),
            callback_query=CallbackQuery.from_dict(data.get("callback_query")),
            inline_query=data.get("inline_query"),
            chosen_inline_result=data.get("chosen_inline_result"),
            shipping_query=data.get("shipping_query"),
            pre_checkout_query=data.get("pre_checkout_query"),
            poll=data.get("poll"),
            poll_answer=data.get("poll_answer"),
            my_chat_member=data.get("my_chat_member"),
            chat_member=data.get("chat_member"),
            chat_join_request=data.get("chat_join_request"),
            business_connection=data.get("business_connection"),
            business_message=Message.from_dict(data.get("business_message")),
            message_reaction=data.get("message_reaction"),
            message_reaction_count=data.get("message_reaction_count"),
            raw=data,
        )

    @property
    def effective_message(self) -> Message | None:
        return (
            self.message
            or self.edited_message
            or self.channel_post
            or self.edited_channel_post
            or self.business_message
            or (self.callback_query.message if self.callback_query else None)
        )

    @property
    def effective_user(self) -> User | None:
        if self.callback_query:
            return self.callback_query.from_user
        msg = self.effective_message
        return msg.from_user if msg else None

    @property
    def effective_chat(self) -> Chat | None:
        msg = self.effective_message
        return msg.chat if msg else None
