# Finite State Machine

```python
from atlib import State, StatesGroup, Application, Command, Text
from atlib.filters.state import StateFilter

class Form(StatesGroup):
    name = State()
    email = State()

app = Application(token=TOKEN)

@app.router.message(Command("form"))
async def begin(ctx):
    await ctx.fsm.set_state(Form.name)
    await ctx.answer("Name?")

@app.router.message(StateFilter(Form.name), Text())
async def name(ctx):
    await ctx.fsm.update_data(name=ctx.message.text)
    await ctx.fsm.set_state(Form.email)
    await ctx.answer("Email?")
```

Storage backends: `MemoryStorage` (default), `SQLiteStorage("fsm.db")`.
