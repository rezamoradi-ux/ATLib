"""Structured logging helpers with token redaction."""

from __future__ import annotations
import logging
import re
from typing import Any

TOKEN_RE = re.compile(r"\d{8,12}:[A-Za-z0-9_-]{30,}")


class TokenRedactingFilter(logging.Filter):
    """Remove bot tokens from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = TOKEN_RE.sub("<REDACTED_TOKEN>", record.msg)
        if record.args:
            new_args = []
            for a in record.args:
                if isinstance(a, str):
                    new_args.append(TOKEN_RE.sub("<REDACTED_TOKEN>", a))
                else:
                    new_args.append(a)
            record.args = tuple(new_args)
        return True


def setup_logging(level: str = "INFO", *, json_logs: bool = False) -> None:
    """Configure root logger for ATLib."""
    root = logging.getLogger("atlib")
    root.handlers.clear()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler()
    if json_logs:
        formatter = logging.Formatter(
            '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    handler.setFormatter(formatter)
    handler.addFilter(TokenRedactingFilter())
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"atlib.{name}")
