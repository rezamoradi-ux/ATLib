"""Telegram Mini App initData validation (official HMAC rules)."""

from __future__ import annotations
import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import parse_qsl
from ..exceptions import ValidationError


def parse_init_data(init_data: str) -> dict[str, Any]:
    """Parse the query-string style initData into a dict."""
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    result: dict[str, Any] = {}
    for k, v in pairs.items():
        if k in ("user", "receiver", "chat"):
            try:
                result[k] = json.loads(v)
            except json.JSONDecodeError:
                result[k] = v
        else:
            result[k] = v
    return result


def validate_init_data(
    init_data: str,
    bot_token: str,
    *,
    max_age: int = 86400,
) -> dict[str, Any]:
    """
    Validate Mini App initData according to Telegram documentation.

    Raises ValidationError on failure.
    Returns parsed data on success.
    """
    if not init_data:
        raise ValidationError("Empty initData")

    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise ValidationError("Missing hash in initData")

    # Build data-check-string
    check_items = sorted(f"{k}={v}" for k, v in parsed.items())
    data_check_string = "\n".join(check_items)

    # Secret key = HMAC_SHA256(<bot_token>, "WebAppData")
    secret_key = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256,
    ).digest()

    computed = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(computed, received_hash):
        raise ValidationError("Invalid initData signature")

    # Auth date check
    auth_date = parsed.get("auth_date")
    if auth_date:
        try:
            ts = int(auth_date)
            if max_age > 0 and (time.time() - ts) > max_age:
                raise ValidationError("initData expired")
        except ValueError:
            raise ValidationError("Invalid auth_date")

    return parse_init_data(init_data)
