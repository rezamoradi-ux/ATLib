"""Custom (Premium) emoji entity support."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class CustomEmoji:
    """
    Represents a custom emoji entity for Telegram messages.

    Uses the official MessageEntity type "custom_emoji".
    The custom_emoji_id must be a valid ID obtained from Telegram.
    Wrapping a normal Unicode emoji does NOT turn it into a Premium emoji.
    """

    emoji: str
    custom_emoji_id: str

    def entity(self, offset: int) -> dict[str, Any]:
        """Build a MessageEntity dict (UTF-16 offset/length)."""
        # Telegram uses UTF-16 code units for offset/length
        length = _utf16_len(self.emoji)
        return {
            "type": "custom_emoji",
            "offset": offset,
            "length": length,
            "custom_emoji_id": self.custom_emoji_id,
        }

    def to_dict(self) -> dict[str, Any]:
        return {"emoji": self.emoji, "custom_emoji_id": self.custom_emoji_id}


def _utf16_len(text: str) -> int:
    """Calculate length in UTF-16 code units as required by Telegram."""
    return len(text.encode("utf-16-le")) // 2
