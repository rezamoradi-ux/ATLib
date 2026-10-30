"""Configuration tests."""

import pytest
from atlib.config import Config
from atlib.exceptions import ConfigurationError


def test_valid_config():
    c = Config(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    assert ":" in c.token
    assert "***" in c.redacted_token() or "..." in c.redacted_token()


def test_invalid_token():
    with pytest.raises(ConfigurationError):
        Config(token="not-a-token")


def test_from_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    c = Config.from_env()
    assert c.token.startswith("123456:")
