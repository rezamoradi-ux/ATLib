"""Inline keyboard example."""

import os
from atlib import Application, Command, InlineKeyboard, InlineButton, CallbackData

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
app = Application(token=TOKEN)


@app.router.message(Command("menu"))
async def menu(ctx):
    kb = InlineKeyboard()
    kb.row(
        InlineButton("Option A", callback_data="opt:a"),
        InlineButton("Option B", callback_data="opt:b"),
    )
    kb.row(InlineButton("Docs", url="https://core.telegram.org/bots/api"))
    await ctx.answer("Choose an option:", reply_markup=kb)


@app.router.callback_query(CallbackData(prefix="opt:"))
async def on_option(ctx):
    data = ctx.callback_query.data
    await ctx.bot.answer_callback_query(ctx.callback_query.id, text=f"Selected {data}")
    await ctx.answer(f"You chose {data}")


if __name__ == "__main__":
    app.run_polling()
