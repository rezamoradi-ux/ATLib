"""Rich message serialization."""

from atlib.rich import RichMessage, TextBlock, ListBlock, TableBlock


def test_rich_message():
    rm = RichMessage()
    rm.text("Hello").list(["a", "b"]).table([["X", "Y"], ["1", "2"]])
    blocks = rm.to_list()
    assert len(blocks) == 3
    assert blocks[0]["type"] == "text"
    assert blocks[1]["type"] == "list"
    assert blocks[2]["type"] == "table"
