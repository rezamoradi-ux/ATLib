"""Exception hierarchy for ATLib."""

from __future__ import annotations
from typing import Any


class ATLibError(Exception):
    """Base exception for all ATLib errors."""

    def __init__(self, message: str = "", *, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(ATLibError):
    """Invalid or missing configuration."""


class ValidationError(ATLibError):
    """Input validation failed."""


class SerializationError(ATLibError):
    """Serialization or deserialization failed."""


class NetworkError(ATLibError):
    """Network-level failure (connection, DNS, TLS, etc.)."""


class TimeoutError(NetworkError):
    """Request timed out."""


class TelegramAPIError(ATLibError):
    """Telegram Bot API returned an error response."""

    def __init__(
        self,
        message: str,
        error_code: int | None = None,
        parameters: dict[str, Any] | None = None,
        *,
        method: str | None = None,
    ):
        super().__init__(message, details={"error_code": error_code, "parameters": parameters})
        self.error_code = error_code
        self.parameters = parameters or {}
        self.method = method
        self.retry_after: float | None = None
        self.migrate_to_chat_id: int | None = None
        if parameters:
            if "retry_after" in parameters:
                self.retry_after = float(parameters["retry_after"])
            if "migrate_to_chat_id" in parameters:
                self.migrate_to_chat_id = int(parameters["migrate_to_chat_id"])


class RateLimitError(TelegramAPIError):
    """HTTP 429 / flood control."""


class AuthenticationError(TelegramAPIError):
    """Invalid token or unauthorized."""


class StorageError(ATLibError):
    """Storage backend failure."""


class PluginError(ATLibError):
    """Plugin loading or execution error."""


class HandlerError(ATLibError):
    """Handler execution error."""


class WebhookError(ATLibError):
    """Webhook validation or processing error."""
