"""Update dispatcher with routing, filters and middleware."""

from __future__ import annotations
import asyncio
import logging
from typing import Any, Callable, Awaitable, Sequence
from dataclasses import dataclass, field

from .types.updates import Update
from .context import Context
from .filters.base import Filter
from .exceptions import HandlerError

log = logging.getLogger("atlib.dispatcher")

HandlerFunc = Callable[..., Awaitable[Any]]


@dataclass
class HandlerRecord:
    callback: HandlerFunc
    filters: list[Filter] = field(default_factory=list)
    priority: int = 0
    update_types: set[str] = field(default_factory=set)
    name: str | None = None


class Router:
    """Composable router for grouping handlers and middleware."""

    def __init__(self, name: str = "default"):
        self.name = name
        self.handlers: list[HandlerRecord] = []
        self.middlewares: list[Callable] = []
        self.sub_routers: list[Router] = []
        self._error_handlers: list[HandlerFunc] = []

    def message(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"message"}, func.__name__)
            )
            return func
        return decorator

    def edited_message(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"edited_message"}, func.__name__)
            )
            return func
        return decorator

    def callback_query(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"callback_query"}, func.__name__)
            )
            return func
        return decorator

    def inline_query(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"inline_query"}, func.__name__)
            )
            return func
        return decorator

    def channel_post(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"channel_post"}, func.__name__)
            )
            return func
        return decorator

    def poll(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"poll"}, func.__name__)
            )
            return func
        return decorator

    def my_chat_member(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"my_chat_member"}, func.__name__)
            )
            return func
        return decorator

    def chat_member(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"chat_member"}, func.__name__)
            )
            return func
        return decorator

    def chat_join_request(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"chat_join_request"}, func.__name__)
            )
            return func
        return decorator

    def pre_checkout_query(self, *filters: Filter, priority: int = 0):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.handlers.append(
                HandlerRecord(func, list(filters), priority, {"pre_checkout_query"}, func.__name__)
            )
            return func
        return decorator

    def error(self):
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self._error_handlers.append(func)
            return func
        return decorator

    def include_router(self, router: Router) -> None:
        self.sub_routers.append(router)

    def middleware(self, func: Callable) -> Callable:
        self.middlewares.append(func)
        return func

    def all_handlers(self) -> list[HandlerRecord]:
        result = list(self.handlers)
        for sub in self.sub_routers:
            result.extend(sub.all_handlers())
        return sorted(result, key=lambda h: -h.priority)


class Dispatcher:
    """Processes updates and dispatches them to matching handlers."""

    def __init__(self, *, concurrent: bool = False, max_workers: int = 4):
        self.router = Router("root")
        self.concurrent = concurrent
        self.max_workers = max_workers
        self._running = False
        self._offset = 0
        self._processed = 0
        self._errors = 0

    def include_router(self, router: Router) -> None:
        self.router.include_router(router)

    def message(self, *filters: Filter, priority: int = 0):
        return self.router.message(*filters, priority=priority)

    def callback_query(self, *filters: Filter, priority: int = 0):
        return self.router.callback_query(*filters, priority=priority)

    def error(self):
        return self.router.error()

    async def feed_update(self, bot: Any, update: Update, *, fsm: Any = None) -> None:
        ctx = Context(bot, update, fsm=fsm)
        handlers = self.router.all_handlers()
        update_type = self._detect_type(update)

        for record in handlers:
            if record.update_types and update_type not in record.update_types:
                continue
            try:
                matched = True
                for f in record.filters:
                    if not await f.check(update, ctx):
                        matched = False
                        break
                if not matched:
                    continue
                await record.callback(ctx)
                self._processed += 1
                return  # first match wins (can be extended)
            except Exception as exc:
                self._errors += 1
                log.exception("Handler %s failed: %s", record.name, exc)
                for err_h in self.router._error_handlers:
                    try:
                        await err_h(ctx, exc)
                    except Exception:
                        log.exception("Error handler failed")
                raise HandlerError(str(exc)) from exc

    def _detect_type(self, update: Update) -> str:
        for name in (
            "message", "edited_message", "channel_post", "edited_channel_post",
            "callback_query", "inline_query", "chosen_inline_result",
            "shipping_query", "pre_checkout_query", "poll", "poll_answer",
            "my_chat_member", "chat_member", "chat_join_request",
            "business_connection", "business_message",
            "message_reaction", "message_reaction_count",
        ):
            if getattr(update, name, None) is not None:
                return name
        return "unknown"

    @property
    def stats(self) -> dict[str, int]:
        return {"processed": self._processed, "errors": self._errors}
