"""Fluent keyboard builder helpers."""

from __future__ import annotations
from .inline import InlineKeyboard, InlineButton
from .reply import ReplyKeyboard, ReplyButton


class KeyboardBuilder:
    @staticmethod
    def inline() -> InlineKeyboard:
        return InlineKeyboard()

    @staticmethod
    def reply() -> ReplyKeyboard:
        return ReplyKeyboard()

    @staticmethod
    def pagination(
        page: int,
        total_pages: int,
        *,
        callback_prefix: str = "page:",
        prev_text: str = "‹",
        next_text: str = "›",
    ) -> InlineKeyboard:
        kb = InlineKeyboard()
        buttons = []
        if page > 1:
            buttons.append(InlineButton(prev_text, callback_data=f"{callback_prefix}{page - 1}"))
        buttons.append(InlineButton(f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            buttons.append(InlineButton(next_text, callback_data=f"{callback_prefix}{page + 1}"))
        kb.row(*buttons)
        return kb
