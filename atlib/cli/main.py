"""ATLib command-line interface."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="atlib",
        description="ATLib — Advanced Telegram Bot Library CLI",
    )
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("doctor", help="Run environment diagnostics")
    init_p = sub.add_parser("init", help="Scaffold a new bot project")
    init_p.add_argument("name", help="Project directory name")
    sub.add_parser("routes", help="List registered routes (placeholder)")
    sub.add_parser("validate", help="Validate package installation")

    args = parser.parse_args(argv)

    if args.version or args.command is None:
        from atlib import __version__, __api_compatibility__
        print(f"ATLib {__version__}")
        print(f"Telegram Bot API compatibility: {__api_compatibility__}")
        return 0

    if args.command == "doctor":
        return _doctor()
    if args.command == "init":
        return _init(args.name)
    if args.command == "validate":
        return _validate()
    if args.command == "routes":
        print("No runtime router attached. Use Application.router in your bot.")
        return 0

    parser.print_help()
    return 1


def _doctor() -> int:
    print("ATLib Doctor")
    print("-" * 40)
    import sys
    print(f"Python: {sys.version}")
    try:
        import httpx
        print(f"httpx:  {httpx.__version__}")
    except ImportError:
        print("httpx:  NOT INSTALLED")
    try:
        import pydantic
        print(f"pydantic: {pydantic.__version__}")
    except ImportError:
        print("pydantic: NOT INSTALLED (optional for some features)")
    from atlib import __version__
    print(f"atlib:  {__version__}")
    print("Status: OK")
    return 0


def _init(name: str) -> int:
    path = Path(name)
    if path.exists():
        print(f"Directory {name} already exists", file=sys.stderr)
        return 1
    path.mkdir(parents=True)
    (path / "bot.py").write_text(
        '''"""Example ATLib bot."""
import asyncio
from atlib import Application, Command

app = Application(token="YOUR_BOT_TOKEN")

@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("Hello from ATLib!")

if __name__ == "__main__":
    app.run_polling()
'''
    )
    (path / "requirements.txt").write_text("atlib-telegram>=1.0.0\n")
    print(f"Created project scaffold in ./{name}/")
    print("Edit bot.py and set your token, then: python bot.py")
    return 0


def _validate() -> int:
    try:
        import atlib
        from atlib import Bot, Application, InlineKeyboard, CustomEmoji
        print(f"atlib {atlib.__version__} imports successfully")
        return 0
    except Exception as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
