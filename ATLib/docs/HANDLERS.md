# Handlers & Routers

```python
from atlib import Application, Command, CallbackData

app = Application(token=TOKEN)

@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("Hi")

@app.router.callback_query(CallbackData(prefix="item:"))
async def on_item(ctx):
    await ctx.bot.answer_callback_query(ctx.callback_query.id)
```

Nested routers:

```python
from atlib.dispatcher import Router
admin = Router("admin")
app.include_router(admin)
```
