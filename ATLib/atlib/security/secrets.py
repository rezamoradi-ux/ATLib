"""Secret redaction utilities."""

from __future__ import annotations
import re

TOKEN_PATTERN = re.compile(r"\d{8,12}:[A-Za-z0-9_-]{20,}")


def redact_secrets(text: str) -> str:
    return TOKEN_PATTERN.sub("<REDACTED>", text)
