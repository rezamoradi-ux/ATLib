"""Rich message blocks (Bot API 10.1+).

This module provides a typed builder that serializes to the official
rich_message schema. Only documented block types are included.
"""

from __future__ import annotations
from typing import Any


class TextBlock:
    def __init__(self, text: str, *, style: str | None = None):
        self.text = text
        self.style = style

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": "text", "text": self.text}
        if self.style:
            d["style"] = self.style
        return d


class ListBlock:
    def __init__(self, items: list[str], *, ordered: bool = False):
        self.items = items
        self.ordered = ordered

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "list",
            "ordered": self.ordered,
            "items": [{"type": "text", "text": i} for i in self.items],
        }


class TableBlock:
    def __init__(self, rows: list[list[str]], *, is_compact: bool = False):
        self.rows = rows
        self.is_compact = is_compact

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "table",
            "is_compact": self.is_compact,
            "rows": [
                [{"type": "text", "text": cell} for cell in row]
                for row in self.rows
            ],
        }


class RichMessage:
    def __init__(self, blocks: list[Any] | None = None):
        self.blocks = blocks or []

    def add(self, block: Any) -> RichMessage:
        self.blocks.append(block)
        return self

    def text(self, content: str, **kwargs: Any) -> RichMessage:
        return self.add(TextBlock(content, **kwargs))

    def list(self, items: list[str], **kwargs: Any) -> RichMessage:
        return self.add(ListBlock(items, **kwargs))

    def table(self, rows: list[list[str]], **kwargs: Any) -> RichMessage:
        return self.add(TableBlock(rows, **kwargs))

    def to_list(self) -> list[dict[str, Any]]:
        result = []
        for b in self.blocks:
            if hasattr(b, "to_dict"):
                result.append(b.to_dict())
            elif isinstance(b, dict):
                result.append(b)
            else:
                result.append({"type": "text", "text": str(b)})
        return result
