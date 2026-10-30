# ATLib — Advanced Telegram Bot Library

**Version 1.0.0** · Official Telegram Bot API · Async · Production-oriented

ATLib is a modular asynchronous Python framework for building Telegram bots using the **official Telegram Bot API**. It does not depend on user account sessions or unofficial clients.

## Features

- Async HTTP transport with connection pooling, rate limiting and retries
- Full update processing (long polling)
- Router / handler system with composable filters
- Inline & reply keyboard builders (including documented style fields)
- Custom (Premium) emoji entities with correct UTF-16 offsets
- Rich message builders (Bot API 10.1+)
- Finite State Machine with Memory and SQLite storage
- Mini App `initData` HMAC validation
- Typed configuration, token redaction, structured logging
- CLI (`atlib doctor`, `atlib init`, …)
- Dual-language docs (English + Persian)

## Installation

```bash
pip install atlib-telegram
# or from source
pip install .
```

Optional extras:

```bash
pip install "atlib-telegram[redis,postgres,dotenv,asgi]"
```

## Quick start

```python
import os
from atlib import Application, Command

app = Application(token=os.environ["BOT_TOKEN"])

@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("Hello from ATLib!")

if __name__ == "__main__":
    app.run_polling()
```

## API compatibility

Verified against **Telegram Bot API 10.3** (August 2026 changelog).  
See [API_COVERAGE.md](API_COVERAGE.md) for the method matrix.

## Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART](docs/QUICKSTART.md) | First bot |
| [HANDLERS](docs/HANDLERS.md) | Routers & handlers |
| [FILTERS](docs/FILTERS.md) | Filters |
| [FSM](docs/FSM.md) | State machine |
| [KEYBOARDS](docs/KEYBOARDS.md) | Keyboards |
| [CUSTOM_EMOJI](docs/CUSTOM_EMOJI.md) | Premium emoji |
| [SECURITY](docs/SECURITY.md) | Security notes |
| [README.fa.md](README.fa.md) | مستندات فارسی |

## License

MIT
