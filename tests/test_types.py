"""Type parsing tests."""

from atlib.types.users import User
from atlib.types.chats import Chat
from atlib.types.messages import Message, MessageEntity
from atlib.types.updates import Update
from atlib.types.callbacks import CallbackQuery


def test_user_from_dict():
    data = {"id": 42, "is_bot": False, "first_name": "Alice", "username": "alice"}
    u = User.from_dict(data)
    assert u is not None
    assert u.id == 42
    assert u.username == "alice"


def test_chat_from_dict():
    data = {"id": -100, "type": "supergroup", "title": "Test"}
    c = Chat.from_dict(data)
    assert c is not None
    assert c.is_group
    assert not c.is_private


def test_message_from_dict():
    data = {
        "message_id": 1,
        "date": 1234567890,
        "chat": {"id": 1, "type": "private"},
        "from": {"id": 2, "is_bot": False, "first_name": "Bob"},
        "text": "hello",
        "entities": [{"type": "bold", "offset": 0, "length": 5}],
    }
    m = Message.from_dict(data)
    assert m is not None
    assert m.text == "hello"
    assert m.content_type == "text"
    assert len(m.entities) == 1


def test_update_from_dict():
    data = {
        "update_id": 100,
        "message": {
            "message_id": 1,
            "date": 1,
            "chat": {"id": 1, "type": "private"},
            "text": "hi",
        },
    }
    u = Update.from_dict(data)
    assert u.update_id == 100
    assert u.effective_message is not None
    assert u.effective_message.text == "hi"


def test_callback_query():
    data = {
        "id": "cq1",
        "from": {"id": 1, "is_bot": False, "first_name": "A"},
        "chat_instance": "ci",
        "data": "btn:1",
    }
    cq = CallbackQuery.from_dict(data)
    assert cq is not None
    assert cq.data == "btn:1"
