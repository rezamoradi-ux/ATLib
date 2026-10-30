"""Reply keyboard builder."""

from __future__ import annotations
from typing import Any


class ReplyButton:
    def __init__(
        self,
        text: str,
        *,
        request_contact: bool | None = None,
        request_location: bool | None = None,
        request_poll: dict | None = None,
        web_app: dict | None = None,
        request_users: dict | None = None,
        request_chat: dict | None = None,
        style: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.web_app = web_app
        self.request_users = request_users
        self.request_chat = request_chat
        self.style = style
        self.icon_custom_emoji_id = icon_custom_emoji_id

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"text": self.text}
        if self.request_contact:
            d["request_contact"] = True
        if self.request_location:
            d["request_location"] = True
        if self.request_poll is not None:
            d["request_poll"] = self.request_poll
        if self.web_app is not None:
            d["web_app"] = self.web_app
        if self.request_users is not None:
            d["request_users"] = self.request_users
        if self.request_chat is not None:
            d["request_chat"] = self.request_chat
        if self.style is not None:
            d["style"] = self.style
        if self.icon_custom_emoji_id is not None:
            d["icon_custom_emoji_id"] = self.icon_custom_emoji_id
        return d


class ReplyKeyboard:
    def __init__(
        self,
        rows: list[list[ReplyButton]] | None = None,
        *,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
        is_persistent: bool | None = None,
        input_field_placeholder: str | None = None,
    ):
        self.rows = rows or []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.is_persistent = is_persistent
        self.input_field_placeholder = input_field_placeholder

    def row(self, *buttons: ReplyButton) -> ReplyKeyboard:
        self.rows.append(list(buttons))
        return self

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "keyboard": [[b.to_dict() for b in row] for row in self.rows],
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard,
            "selective": self.selective,
        }
        if self.is_persistent is not None:
            d["is_persistent"] = self.is_persistent
        if self.input_field_placeholder:
            d["input_field_placeholder"] = self.input_field_placeholder
        return d


class RemoveKeyboard:
    def __init__(self, selective: bool = False):
        self.selective = selective

    def to_dict(self) -> dict[str, Any]:
        return {"remove_keyboard": True, "selective": self.selective}
