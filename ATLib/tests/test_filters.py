"""Filter tests."""

import pytest
from atlib.filters import Command, Text, ExactText, Regex, Private, Group, CallbackData
from atlib.types.updates import Update
from atlib.context import Context
from atlib.bot import Bot


def _make_update(text=None, chat_type="private", callback_data=None):
    data = {"update_id": 1}
    if text is not None:
        data["message"] = {
            "message_id": 1,
            "date": 1,
            "chat": {"id": 1, "type": chat_type},
            "from": {"id": 10, "is_bot": False, "first_name": "U"},
            "text": text,
        }
    if callback_data is not None:
        data["callback_query"] = {
            "id": "c1",
            "from": {"id": 10, "is_bot": False, "first_name": "U"},
            "chat_instance": "x",
            "data": callback_data,
        }
    return Update.from_dict(data)


@pytest.fixture
def bot():
    return Bot(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


@pytest.mark.asyncio
async def test_command_filter(bot):
    f = Command("start", "help")
    ctx = Context(bot, _make_update("/start"))
    assert await f.check(ctx.update, ctx)
    ctx2 = Context(bot, _make_update("/unknown"))
    assert not await f.check(ctx2.update, ctx2)


@pytest.mark.asyncio
async def test_exact_text(bot):
    f = ExactText("hello")
    ctx = Context(bot, _make_update("hello"))
    assert await f.check(ctx.update, ctx)


@pytest.mark.asyncio
async def test_regex(bot):
    f = Regex(r"^order\s+\d+$")
    ctx = Context(bot, _make_update("order 42"))
    assert await f.check(ctx.update, ctx)


@pytest.mark.asyncio
async def test_private(bot):
    f = Private()
    ctx = Context(bot, _make_update("hi", chat_type="private"))
    assert await f.check(ctx.update, ctx)
    ctx2 = Context(bot, _make_update("hi", chat_type="group"))
    assert not await f.check(ctx2.update, ctx2)


@pytest.mark.asyncio
async def test_callback_data(bot):
    f = CallbackData(prefix="page:")
    ctx = Context(bot, _make_update(callback_data="page:3"))
    assert await f.check(ctx.update, ctx)


@pytest.mark.asyncio
async def test_and_or(bot):
    f = Command("start") & Private()
    ctx = Context(bot, _make_update("/start", chat_type="private"))
    assert await f.check(ctx.update, ctx)
