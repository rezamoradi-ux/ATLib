"""Webhook secret token validation."""

from __future__ import annotations
import hmac
from ..exceptions import WebhookError


def validate_webhook_secret(
    received: str | None,
    expected: str | None,
) -> None:
    if not expected:
        return  # secret not configured
    if not received:
        raise WebhookError("Missing X-Telegram-Bot-Api-Secret-Token header")
    if not hmac.compare_digest(received, expected):
        raise WebhookError("Invalid webhook secret token")
