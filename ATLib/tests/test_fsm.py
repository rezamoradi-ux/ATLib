"""FSM tests."""

import pytest
from atlib.fsm import State, StatesGroup, FSMContext
from atlib.storage.memory import MemoryStorage
from atlib.storage.sqlite import SQLiteStorage
import tempfile
import os


class Reg(StatesGroup):
    name = State()
    age = State()


@pytest.mark.asyncio
async def test_memory_fsm():
    storage = MemoryStorage()
    ctx = FSMContext(storage, "user:1")
    await ctx.set_state(Reg.name)
    assert await ctx.get_state() == "Reg:name"
    await ctx.update_data(name="Alice")
    data = await ctx.get_data()
    assert data["name"] == "Alice"
    await ctx.clear()
    assert await ctx.get_state() is None


@pytest.mark.asyncio
async def test_sqlite_fsm():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = f.name
    try:
        storage = SQLiteStorage(path)
        ctx = FSMContext(storage, "user:42")
        await ctx.set_state(Reg.age)
        assert await ctx.get_state() == "Reg:age"
        await ctx.set_data({"age": 30})
        assert (await ctx.get_data())["age"] == 30
        await ctx.clear()
        await storage.close()
    finally:
        os.unlink(path)


def test_state_str():
    assert str(Reg.name) == "Reg:name"
