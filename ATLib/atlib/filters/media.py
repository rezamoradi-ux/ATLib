"""Media content type filters."""

from __future__ import annotations
from .base import Filter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class _ContentTypeFilter(Filter):
    content_type: str

    async def check(self, update: Update, ctx: Context) -> bool:
        msg = update.effective_message
        return bool(msg and msg.content_type == self.content_type)


class Photo(_ContentTypeFilter):
    content_type = "photo"


class Video(_ContentTypeFilter):
    content_type = "video"


class Document(_ContentTypeFilter):
    content_type = "document"


class Audio(_ContentTypeFilter):
    content_type = "audio"


class Voice(_ContentTypeFilter):
    content_type = "voice"


class Sticker(_ContentTypeFilter):
    content_type = "sticker"


class Animation(_ContentTypeFilter):
    content_type = "animation"
