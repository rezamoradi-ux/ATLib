# Quick Start

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. Install:

```bash
pip install atlib-telegram
```

3. Create `bot.py`:

```python
import os
from atlib import Application, Command

app = Application(token=os.environ["BOT_TOKEN"])

@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("Hello!")

if __name__ == "__main__":
    app.run_polling()
```

4. Run:

```bash
export BOT_TOKEN="123456:ABC..."
python bot.py
```
