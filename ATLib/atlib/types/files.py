"""File and media size types."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PhotoSize:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data["width"],
            height=data["height"],
            file_size=data.get("file_size"),
            raw=data,
        )


@dataclass
class File:
    file_id: str
    file_unique_id: str
    file_size: int | None = None
    file_path: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> File:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            file_size=data.get("file_size"),
            file_path=data.get("file_path"),
            raw=data,
        )
