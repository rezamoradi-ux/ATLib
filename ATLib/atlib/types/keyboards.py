"""Keyboard markup type stubs used by serialization."""

from __future__ import annotations
from typing import Any


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: list[list[dict[str, Any]]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self) -> dict[str, Any]:
        return {"inline_keyboard": self.inline_keyboard}


class ReplyKeyboardMarkup:
    def __init__(self, keyboard: list[list[dict[str, Any]]], **kwargs: Any):
        self.keyboard = keyboard
        self.kwargs = kwargs

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"keyboard": self.keyboard}
        d.update(self.kwargs)
        return d
