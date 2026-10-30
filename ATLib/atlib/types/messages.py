"""Message and entity types."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .users import User
from .chats import Chat


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int
    url: str | None = None
    user: User | None = None
    language: str | None = None
    custom_emoji_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MessageEntity:
        return cls(
            type=data["type"],
            offset=data["offset"],
            length=data["length"],
            url=data.get("url"),
            user=User.from_dict(data.get("user")),
            language=data.get("language"),
            custom_emoji_id=data.get("custom_emoji_id"),
            raw=data,
        )

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self.type,
            "offset": self.offset,
            "length": self.length,
        }
        if self.url:
            d["url"] = self.url
        if self.user:
            d["user"] = self.user.to_dict()
        if self.language:
            d["language"] = self.language
        if self.custom_emoji_id:
            d["custom_emoji_id"] = self.custom_emoji_id
        return d


@dataclass
class Message:
    message_id: int
    date: int
    chat: Chat
    from_user: User | None = None
    text: str | None = None
    caption: str | None = None
    entities: list[MessageEntity] = field(default_factory=list)
    caption_entities: list[MessageEntity] = field(default_factory=list)
    reply_to_message: Message | None = None
    edit_date: int | None = None
    media_group_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Message | None:
        if not data:
            return None
        entities = [MessageEntity.from_dict(e) for e in data.get("entities", [])]
        caption_entities = [MessageEntity.from_dict(e) for e in data.get("caption_entities", [])]
        return cls(
            message_id=data["message_id"],
            date=data.get("date", 0),
            chat=Chat.from_dict(data["chat"]) or Chat(id=0, type="private"),
            from_user=User.from_dict(data.get("from")),
            text=data.get("text"),
            caption=data.get("caption"),
            entities=entities,
            caption_entities=caption_entities,
            reply_to_message=Message.from_dict(data.get("reply_to_message")),
            edit_date=data.get("edit_date"),
            media_group_id=data.get("media_group_id"),
            raw=data,
        )

    @property
    def content_type(self) -> str:
        raw = self.raw
        for key in (
            "text", "photo", "video", "audio", "voice", "document",
            "sticker", "animation", "video_note", "contact", "location",
            "venue", "poll", "dice", "new_chat_members", "left_chat_member",
            "invoice", "successful_payment", "rich_message",
        ):
            if key in raw and raw[key] is not None:
                return key
        return "unknown"
