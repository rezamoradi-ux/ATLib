"""Helpers for building message entities with correct UTF-16 offsets."""

from __future__ import annotations
from typing import Any
from .custom import CustomEmoji, _utf16_len


def build_entities(parts: list[str | CustomEmoji]) -> tuple[str, list[dict[str, Any]]]:
    """
    Concatenate text parts and CustomEmoji objects into a single string
    plus a list of MessageEntity dicts with correct UTF-16 offsets.
    """
    text_parts: list[str] = []
    entities: list[dict[str, Any]] = []
    offset = 0
    for part in parts:
        if isinstance(part, CustomEmoji):
            text_parts.append(part.emoji)
            entities.append(part.entity(offset))
            offset += _utf16_len(part.emoji)
        else:
            text_parts.append(part)
            offset += _utf16_len(part)
    return "".join(text_parts), entities
