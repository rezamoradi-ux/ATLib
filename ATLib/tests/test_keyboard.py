"""Keyboard serialization tests."""

from atlib.keyboards import InlineKeyboard, InlineButton, ReplyKeyboard, ReplyButton, RemoveKeyboard


def test_inline_keyboard():
    kb = InlineKeyboard()
    kb.row(
        InlineButton("Yes", callback_data="yes"),
        InlineButton("No", callback_data="no"),
    )
    kb.row(InlineButton("Docs", url="https://core.telegram.org/bots/api"))
    d = kb.to_dict()
    assert "inline_keyboard" in d
    assert len(d["inline_keyboard"]) == 2
    assert d["inline_keyboard"][0][0]["callback_data"] == "yes"
    assert d["inline_keyboard"][1][0]["url"].startswith("https://")


def test_inline_style_fields():
    btn = InlineButton("Go", callback_data="go", style="primary", icon_custom_emoji_id="123")
    d = btn.to_dict()
    assert d["style"] == "primary"
    assert d["icon_custom_emoji_id"] == "123"


def test_reply_keyboard():
    kb = ReplyKeyboard()
    kb.row(ReplyButton("Share contact", request_contact=True))
    d = kb.to_dict()
    assert d["resize_keyboard"] is True
    assert d["keyboard"][0][0]["request_contact"] is True


def test_remove_keyboard():
    d = RemoveKeyboard().to_dict()
    assert d["remove_keyboard"] is True
