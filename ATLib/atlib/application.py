"""High-level Application that ties Bot + Dispatcher + lifecycle."""

from __future__ import annotations
import asyncio
import logging
import signal
from typing import Any, Callable, Awaitable

from .bot import Bot
from .dispatcher import Dispatcher, Router
from .config import Config
from .fsm.manager import FSMManager
from .storage.memory import MemoryStorage
from .storage.base import BaseStorage
from .logging import setup_logging, get_logger

log = get_logger("application")


class Application:
    """
    Production-oriented application runner.

    Supports long polling, graceful shutdown, multi-bot isolation,
    and optional FSM storage.
    """

    def __init__(
        self,
        bot: Bot | None = None,
        *,
        token: str | None = None,
        config: Config | None = None,
        storage: BaseStorage | None = None,
        concurrent: bool = False,
    ):
        if bot is None:
            bot = Bot(token=token, config=config)
        self.bot = bot
        self.dispatcher = Dispatcher(concurrent=concurrent)
        self.storage = storage or MemoryStorage()
        self.fsm = FSMManager(self.storage)
        self._tasks: list[asyncio.Task] = []
        self._stop_event = asyncio.Event()
        self._started = False

    @property
    def router(self) -> Router:
        return self.dispatcher.router

    def include_router(self, router: Router) -> None:
        self.dispatcher.include_router(router)

    async def start_polling(self, *, allowed_updates: list[str] | None = None) -> None:
        setup_logging(self.bot.config.log_level)
        log.info("Starting polling (token=%s)", self.bot.config.redacted_token())
        await self.bot.transport.open()
        me = await self.bot.get_me()
        log.info("Bot @%s (id=%s) started", me.username, me.id)

        # Drop pending if configured
        if self.bot.config.drop_pending_updates:
            await self.bot.delete_webhook(drop_pending_updates=True)

        self._stop_event.clear()
        self._started = True
        offset = 0
        allowed = allowed_updates or self.bot.config.allowed_updates

        try:
            while not self._stop_event.is_set():
                try:
                    updates = await self.bot.get_updates(
                        offset=offset,
                        limit=self.bot.config.polling_limit,
                        timeout=self.bot.config.polling_timeout,
                        allowed_updates=allowed,
                    )
                    for update in updates:
                        offset = update.update_id + 1
                        fsm_ctx = await self.fsm.get_context(update)
                        try:
                            await self.dispatcher.feed_update(self.bot, update, fsm=fsm_ctx)
                        except Exception:
                            log.exception("Error processing update %s", update.update_id)
                except asyncio.CancelledError:
                    break
                except Exception:
                    log.exception("Polling error, retrying in 3s")
                    await asyncio.sleep(3)
        finally:
            self._started = False
            log.info("Polling stopped. Stats: %s", self.dispatcher.stats)

    async def stop(self) -> None:
        log.info("Stopping application...")
        self._stop_event.set()
        for t in self._tasks:
            t.cancel()
        await self.bot.close()
        await self.storage.close()

    def run_polling(self, **kwargs: Any) -> None:
        """Blocking entry point."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def _signal_handler():
            loop.create_task(self.stop())

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _signal_handler)
            except NotImplementedError:
                pass

        try:
            loop.run_until_complete(self.start_polling(**kwargs))
        finally:
            loop.run_until_complete(self.stop())
            loop.close()
