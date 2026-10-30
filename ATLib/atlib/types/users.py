"""User-related types."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_inline_queries: bool | None = None
    can_connect_to_business: bool | None = None
    has_main_web_app: bool | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> User | None:
        if not data:
            return None
        return cls(
            id=data["id"],
            is_bot=data.get("is_bot", False),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name"),
            username=data.get("username"),
            language_code=data.get("language_code"),
            is_premium=data.get("is_premium"),
            added_to_attachment_menu=data.get("added_to_attachment_menu"),
            can_join_groups=data.get("can_join_groups"),
            can_read_all_group_messages=data.get("can_read_all_group_messages"),
            supports_inline_queries=data.get("supports_inline_queries"),
            can_connect_to_business=data.get("can_connect_to_business"),
            has_main_web_app=data.get("has_main_web_app"),
            raw=data,
        )

    def to_dict(self) -> dict[str, Any]:
        return self.raw or {
            "id": self.id,
            "is_bot": self.is_bot,
            "first_name": self.first_name,
            **{k: v for k, v in {
                "last_name": self.last_name,
                "username": self.username,
                "language_code": self.language_code,
                "is_premium": self.is_premium,
            }.items() if v is not None},
        }
