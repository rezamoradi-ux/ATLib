"""Typed configuration for ATLib bots."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import os
from .exceptions import ConfigurationError


@dataclass
class Config:
    """Runtime configuration for a Bot / Application."""

    token: str
    base_url: str = "https://api.telegram.org"
    timeout: float = 30.0
    connect_timeout: float = 10.0
    proxy: str | None = None
    verify_tls: bool = True
    allowed_updates: list[str] | None = None
    drop_pending_updates: bool = False
    polling_timeout: int = 30
    polling_limit: int = 100
    worker_count: int = 4
    max_retries: int = 3
    retry_backoff: float = 0.5
    rate_limit_per_second: float = 25.0
    log_level: str = "INFO"
    redact_token: bool = True
    storage_dsn: str | None = None
    webhook_secret: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.token or ":" not in self.token:
            raise ConfigurationError("Bot token must be in the form <bot_id>:<secret>")
        if self.timeout <= 0:
            raise ConfigurationError("timeout must be positive")

    @classmethod
    def from_env(cls, prefix: str = "ATLIB_") -> Config:
        """Load configuration from environment variables."""
        token = os.environ.get(f"{prefix}BOT_TOKEN") or os.environ.get("BOT_TOKEN")
        if not token:
            raise ConfigurationError(
                f"Missing bot token. Set {prefix}BOT_TOKEN or BOT_TOKEN environment variable."
            )
        return cls(
            token=token,
            base_url=os.environ.get(f"{prefix}BASE_URL", "https://api.telegram.org"),
            timeout=float(os.environ.get(f"{prefix}TIMEOUT", "30")),
            proxy=os.environ.get(f"{prefix}PROXY"),
            webhook_secret=os.environ.get(f"{prefix}WEBHOOK_SECRET"),
            storage_dsn=os.environ.get(f"{prefix}STORAGE_DSN"),
            log_level=os.environ.get(f"{prefix}LOG_LEVEL", "INFO"),
        )

    def redacted_token(self) -> str:
        """Return a safe representation of the token for logging."""
        if not self.redact_token or ":" not in self.token:
            return "***"
        bot_id, secret = self.token.split(":", 1)
        if len(secret) <= 6:
            return f"{bot_id}:***"
        return f"{bot_id}:{secret[:3]}...{secret[-3:]}"
