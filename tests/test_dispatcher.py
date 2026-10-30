"""Dispatcher / router tests."""

import pytest
from atlib.dispatcher import Dispatcher, Router
from atlib.filters import Command
from atlib.types.updates import Update
from atlib.bot import Bot
from atlib.context import Context


@pytest.mark.asyncio
async def test_handler_called():
    bot = Bot(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    dp = Dispatcher()
    called = []

    @dp.message(Command("start"))
    async def on_start(ctx: Context):
        called.append(True)

    update = Update.from_dict({
        "update_id": 1,
        "message": {
            "message_id": 1,
            "date": 1,
            "chat": {"id": 1, "type": "private"},
            "from": {"id": 1, "is_bot": False, "first_name": "T"},
            "text": "/start",
        },
    })
    await dp.feed_update(bot, update)
    assert called == [True]
    assert dp.stats["processed"] == 1
