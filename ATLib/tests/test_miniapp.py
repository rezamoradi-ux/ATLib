"""Mini App validation tests."""

import hashlib
import hmac
import time
from urllib.parse import urlencode
import pytest
from atlib.miniapp import validate_init_data, parse_init_data
from atlib.exceptions import ValidationError


def _sign(bot_token: str, fields: dict) -> str:
    check = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    return hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()


def test_validate_ok():
    token = "123456:ABC-DEF"
    fields = {
        "auth_date": str(int(time.time())),
        "user": '{"id":1,"first_name":"A"}',
    }
    fields["hash"] = _sign(token, fields)
    init_data = urlencode(fields)
    result = validate_init_data(init_data, token)
    assert "user" in result


def test_validate_bad_hash():
    token = "123456:ABC-DEF"
    fields = {"auth_date": str(int(time.time())), "hash": "deadbeef"}
    init_data = urlencode(fields)
    with pytest.raises(ValidationError):
        validate_init_data(init_data, token)


def test_parse():
    data = parse_init_data("user=%7B%22id%22%3A1%7D&auth_date=1")
    assert data["user"]["id"] == 1
