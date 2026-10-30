"""Chat-related types."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .users import User


@dataclass
class Chat:
    id: int
    type: str  # private, group, supergroup, channel
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: bool | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Chat | None:
        if not data:
            return None
        return cls(
            id=data["id"],
            type=data.get("type", "private"),
            title=data.get("title"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            is_forum=data.get("is_forum"),
            raw=data,
        )

    @property
    def is_private(self) -> bool:
        return self.type == "private"

    @property
    def is_group(self) -> bool:
        return self.type in ("group", "supergroup")

    @property
    def is_channel(self) -> bool:
        return self.type == "channel"
