"""
ATLib — Advanced Telegram Bot Library

A production-oriented asynchronous Python framework for building bots
with the official Telegram Bot API.
"""

from __future__ import annotations

__version__ = "1.0.0"
__api_compatibility__ = "Bot API 10.3 (verified 2026-10)"

from .bot import Bot
from .application import Application
from .context import Context
from .dispatcher import Dispatcher
from .config import Config
from .exceptions import (
    ATLibError,
    ConfigurationError,
    ValidationError,
    TelegramAPIError,
    NetworkError,
    TimeoutError,
    RateLimitError,
    AuthenticationError,
    SerializationError,
    StorageError,
    PluginError,
    HandlerError,
    WebhookError,
)

from .keyboards.inline import InlineKeyboard, InlineButton
from .keyboards.reply import ReplyKeyboard, ReplyButton, RemoveKeyboard
from .emoji.custom import CustomEmoji
from .filters.base import Filter
from .filters.command import Command
from .filters.text import Text, ExactText, Regex
from .filters.chat import Private, Group, Supergroup, Channel
from .filters.user import UserId, Username
from .filters.callback import CallbackData
from .filters.media import Photo, Video, Document, Audio, Voice, Sticker, Animation
from .fsm.context import FSMContext
from .fsm.states import State, StatesGroup
from .storage.memory import MemoryStorage
from .storage.sqlite import SQLiteStorage
from .types.updates import Update
from .types.messages import Message
from .types.users import User
from .types.chats import Chat
from .types.callbacks import CallbackQuery

__all__ = [
    "__version__",
    "__api_compatibility__",
    "Bot",
    "Application",
    "Context",
    "Dispatcher",
    "Config",
    "ATLibError",
    "ConfigurationError",
    "ValidationError",
    "TelegramAPIError",
    "NetworkError",
    "TimeoutError",
    "RateLimitError",
    "AuthenticationError",
    "SerializationError",
    "StorageError",
    "PluginError",
    "HandlerError",
    "WebhookError",
    "InlineKeyboard",
    "InlineButton",
    "ReplyKeyboard",
    "ReplyButton",
    "RemoveKeyboard",
    "CustomEmoji",
    "Filter",
    "Command",
    "Text",
    "ExactText",
    "Regex",
    "Private",
    "Group",
    "Supergroup",
    "Channel",
    "UserId",
    "Username",
    "CallbackData",
    "Photo",
    "Video",
    "Document",
    "Audio",
    "Voice",
    "Sticker",
    "Animation",
    "FSMContext",
    "State",
    "StatesGroup",
    "MemoryStorage",
    "SQLiteStorage",
    "Update",
    "Message",
    "User",
    "Chat",
    "CallbackQuery",
]
