"""Minimal ATLib bot example.

Set BOT_TOKEN environment variable before running.
"""

import os
from atlib import Application, Command

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
app = Application(token=TOKEN)


@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("Welcome to ATLib! Send /help for commands.")


@app.router.message(Command("help"))
async def help_cmd(ctx):
    await ctx.answer("Commands: /start, /help, /echo")


@app.router.message()
async def echo(ctx):
    if ctx.message and ctx.message.text:
        await ctx.reply(f"You said: {ctx.message.text}")


if __name__ == "__main__":
    app.run_polling()
