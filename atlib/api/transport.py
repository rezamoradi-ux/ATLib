"""Async HTTP transport for Telegram Bot API."""

from __future__ import annotations
import json
import logging
from typing import Any, BinaryIO
import httpx
from ..exceptions import (
    TelegramAPIError,
    NetworkError,
    TimeoutError,
    RateLimitError,
    AuthenticationError,
    SerializationError,
)
from .rate_limiter import RateLimiter
from .retry import RetryPolicy

log = logging.getLogger("atlib.transport")


class Transport:
    """Low-level HTTP client for api.telegram.org."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://api.telegram.org",
        timeout: float = 30.0,
        connect_timeout: float = 10.0,
        proxy: str | None = None,
        verify: bool = True,
        rate_limit: float = 25.0,
        max_retries: int = 3,
    ):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None
        self._proxy = proxy
        self._verify = verify
        self._connect_timeout = connect_timeout
        self.rate_limiter = RateLimiter(rate_limit)
        self.retry = RetryPolicy(max_retries=max_retries)

    async def __aenter__(self) -> Transport:
        await self.open()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def open(self) -> None:
        if self._client is not None:
            return
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
        timeout = httpx.Timeout(self.timeout, connect=self._connect_timeout)
        self._client = httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            proxy=self._proxy,
            verify=self._verify,
            follow_redirects=True,
        )

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _url(self, method: str) -> str:
        return f"{self.base_url}/bot{self.token}/{method}"

    async def request(
        self,
        method: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        *,
        timeout: float | None = None,
    ) -> Any:
        await self.open()
        assert self._client is not None

        async def _do() -> Any:
            await self.rate_limiter.acquire()
            url = self._url(method)
            req_timeout = timeout or self.timeout
            try:
                if files:
                    # Multipart
                    form_data = {}
                    file_parts = {}
                    for k, v in (data or {}).items():
                        if isinstance(v, (dict, list)):
                            form_data[k] = json.dumps(v)
                        else:
                            form_data[k] = str(v) if v is not None else ""
                    for name, fobj in files.items():
                        file_parts[name] = fobj
                    response = await self._client.post(
                        url,
                        data=form_data,
                        files=file_parts,
                        timeout=req_timeout,
                    )
                else:
                    # JSON body preferred for modern API
                    payload = data or {}
                    # Convert nested structures
                    clean: dict[str, Any] = {}
                    for k, v in payload.items():
                        if v is None:
                            continue
                        if hasattr(v, "to_dict"):
                            clean[k] = v.to_dict()
                        else:
                            clean[k] = v
                    response = await self._client.post(
                        url,
                        json=clean,
                        timeout=req_timeout,
                    )
            except httpx.TimeoutException as exc:
                raise TimeoutError(f"Request to {method} timed out") from exc
            except httpx.RequestError as exc:
                raise NetworkError(f"Network error calling {method}: {exc}") from exc

            return self._parse_response(method, response)

        return await self.retry.run(_do)

    def _parse_response(self, method: str, response: httpx.Response) -> Any:
        try:
            payload = response.json()
        except Exception as exc:
            raise SerializationError(f"Invalid JSON from Telegram for {method}") from exc

        if not isinstance(payload, dict):
            raise SerializationError(f"Unexpected response type for {method}")

        if not payload.get("ok"):
            description = payload.get("description", "Unknown Telegram error")
            error_code = payload.get("error_code")
            parameters = payload.get("parameters")
            if error_code == 401:
                raise AuthenticationError(description, error_code, parameters, method=method)
            if error_code == 429:
                raise RateLimitError(description, error_code, parameters, method=method)
            raise TelegramAPIError(description, error_code, parameters, method=method)

        return payload.get("result")

    async def download_file(self, file_path: str) -> bytes:
        await self.open()
        assert self._client is not None
        url = f"{self.base_url}/file/bot{self.token}/{file_path}"
        try:
            response = await self._client.get(url)
            response.raise_for_status()
            return response.content
        except httpx.TimeoutException as exc:
            raise TimeoutError("File download timed out") from exc
        except httpx.RequestError as exc:
            raise NetworkError(f"File download failed: {exc}") from exc
