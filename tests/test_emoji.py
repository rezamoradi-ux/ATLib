"""Custom emoji and UTF-16 offset tests."""

from atlib.emoji import CustomEmoji, build_entities
from atlib.emoji.custom import _utf16_len


def test_utf16_len_ascii():
    assert _utf16_len("hello") == 5


def test_utf16_len_emoji():
    # 🔥 is one Unicode scalar but may be one or two UTF-16 units
    assert _utf16_len("🔥") >= 1


def test_custom_emoji_entity():
    ce = CustomEmoji(emoji="🔥", custom_emoji_id="5368324170671202286")
    ent = ce.entity(0)
    assert ent["type"] == "custom_emoji"
    assert ent["custom_emoji_id"] == "5368324170671202286"
    assert ent["offset"] == 0
    assert ent["length"] == _utf16_len("🔥")


def test_build_entities():
    text, entities = build_entities([
        "Hello ",
        CustomEmoji("🔥", "123"),
        " world",
    ])
    assert text == "Hello 🔥 world"
    assert len(entities) == 1
    assert entities[0]["offset"] == _utf16_len("Hello ")
