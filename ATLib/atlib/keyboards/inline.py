"""Inline keyboard builder supporting official Bot API button fields."""

from __future__ import annotations
from typing import Any


class InlineButton:
    """
    Inline keyboard button.

    Only fields documented by the official Telegram Bot API are exposed.
    Style / icon_custom_emoji_id are available when the client supports them
    (Bot API 9.4+). Telegram controls final rendering.
    """

    def __init__(
        self,
        text: str,
        *,
        callback_data: str | None = None,
        url: str | None = None,
        login_url: dict | None = None,
        web_app: dict | None = None,
        switch_inline_query: str | None = None,
        switch_inline_query_current_chat: str | None = None,
        switch_inline_query_chosen_chat: dict | None = None,
        callback_game: dict | None = None,
        pay: bool | None = None,
        copy_text: dict | None = None,
        style: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.login_url = login_url
        self.web_app = web_app
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.switch_inline_query_chosen_chat = switch_inline_query_chosen_chat
        self.callback_game = callback_game
        self.pay = pay
        self.copy_text = copy_text
        self.style = style
        self.icon_custom_emoji_id = icon_custom_emoji_id

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"text": self.text}
        if self.callback_data is not None:
            d["callback_data"] = self.callback_data
        if self.url is not None:
            d["url"] = self.url
        if self.login_url is not None:
            d["login_url"] = self.login_url
        if self.web_app is not None:
            d["web_app"] = self.web_app
        if self.switch_inline_query is not None:
            d["switch_inline_query"] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            d["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        if self.switch_inline_query_chosen_chat is not None:
            d["switch_inline_query_chosen_chat"] = self.switch_inline_query_chosen_chat
        if self.callback_game is not None:
            d["callback_game"] = self.callback_game
        if self.pay is not None:
            d["pay"] = self.pay
        if self.copy_text is not None:
            d["copy_text"] = self.copy_text
        if self.style is not None:
            d["style"] = self.style
        if self.icon_custom_emoji_id is not None:
            d["icon_custom_emoji_id"] = self.icon_custom_emoji_id
        return d


class InlineKeyboard:
    def __init__(self, rows: list[list[InlineButton]] | None = None):
        self.rows: list[list[InlineButton]] = rows or []

    def row(self, *buttons: InlineButton) -> InlineKeyboard:
        self.rows.append(list(buttons))
        return self

    def add(self, *buttons: InlineButton) -> InlineKeyboard:
        if not self.rows:
            self.rows.append([])
        self.rows[-1].extend(buttons)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "inline_keyboard": [
                [b.to_dict() for b in row] for row in self.rows
            ]
        }

    def adjust(self, *sizes: int) -> InlineKeyboard:
        """Re-pack buttons into rows of the given sizes."""
        flat = [b for row in self.rows for b in row]
        self.rows = []
        idx = 0
        for size in sizes:
            self.rows.append(flat[idx:idx + size])
            idx += size
        if idx < len(flat):
            self.rows.append(flat[idx:])
        return self
