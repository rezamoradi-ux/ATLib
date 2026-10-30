"""FSM registration flow example."""

import os
from atlib import Application, Command, State, StatesGroup, Text
from atlib.filters.state import StateFilter

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
app = Application(token=TOKEN)


class Reg(StatesGroup):
    name = State()
    age = State()


@app.router.message(Command("register"))
async def start_reg(ctx):
    await ctx.fsm.set_state(Reg.name)
    await ctx.answer("What is your name?")


@app.router.message(StateFilter(Reg.name), Text())
async def got_name(ctx):
    await ctx.fsm.update_data(name=ctx.message.text)
    await ctx.fsm.set_state(Reg.age)
    await ctx.answer("How old are you?")


@app.router.message(StateFilter(Reg.age), Text())
async def got_age(ctx):
    data = await ctx.fsm.update_data(age=ctx.message.text)
    await ctx.fsm.clear()
    await ctx.answer(f"Registered: {data['name']}, age {data['age']}")


if __name__ == "__main__":
    app.run_polling()
