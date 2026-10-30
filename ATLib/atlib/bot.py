"""Core asynchronous Bot client for the official Telegram Bot API."""

from __future__ import annotations
import logging
from typing import Any, BinaryIO, Iterable
from pathlib import Path

from .api.transport import Transport
from .config import Config
from .exceptions import ConfigurationError
from .types.messages import Message
from .types.users import User
from .types.files import File
from .types.updates import Update

log = logging.getLogger("atlib.bot")


class Bot:
    """
    High-level asynchronous client for the Telegram Bot API.

    Provides typed method wrappers, automatic serialization, rate limiting,
    retries, and safe resource management.
    """

    def __init__(
        self,
        token: str | None = None,
        *,
        config: Config | None = None,
        **kwargs: Any,
    ):
        if config is None:
            if not token:
                raise ConfigurationError("token or config is required")
            config = Config(token=token, **kwargs)
        self.config = config
        self.transport = Transport(
            token=config.token,
            base_url=config.base_url,
            timeout=config.timeout,
            connect_timeout=config.connect_timeout,
            proxy=config.proxy,
            verify=config.verify_tls,
            rate_limit=config.rate_limit_per_second,
            max_retries=config.max_retries,
        )
        self._me: User | None = None

    async def __aenter__(self) -> Bot:
        await self.transport.open()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def close(self) -> None:
        await self.transport.close()

    async def call(self, method: str, data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        return await self.transport.request(method, data, **kwargs)

    # ── Getting updates ──────────────────────────────────────────────

    async def get_updates(
        self,
        *,
        offset: int | None = None,
        limit: int = 100,
        timeout: int = 30,
        allowed_updates: list[str] | None = None,
    ) -> list[Update]:
        data: dict[str, Any] = {"limit": limit, "timeout": timeout}
        if offset is not None:
            data["offset"] = offset
        if allowed_updates is not None:
            data["allowed_updates"] = allowed_updates
        result = await self.call("getUpdates", data, timeout=timeout + 5)
        return [Update.from_dict(u) for u in (result or [])]

    async def set_webhook(
        self,
        url: str,
        *,
        certificate: Any = None,
        ip_address: str | None = None,
        max_connections: int | None = None,
        allowed_updates: list[str] | None = None,
        drop_pending_updates: bool | None = None,
        secret_token: str | None = None,
    ) -> bool:
        data: dict[str, Any] = {"url": url}
        if ip_address:
            data["ip_address"] = ip_address
        if max_connections is not None:
            data["max_connections"] = max_connections
        if allowed_updates is not None:
            data["allowed_updates"] = allowed_updates
        if drop_pending_updates is not None:
            data["drop_pending_updates"] = drop_pending_updates
        if secret_token:
            data["secret_token"] = secret_token
        return await self.call("setWebhook", data)

    async def delete_webhook(self, *, drop_pending_updates: bool = False) -> bool:
        return await self.call("deleteWebhook", {"drop_pending_updates": drop_pending_updates})

    async def get_webhook_info(self) -> dict[str, Any]:
        return await self.call("getWebhookInfo")

    # ── Available methods ────────────────────────────────────────────

    async def get_me(self) -> User:
        result = await self.call("getMe")
        self._me = User.from_dict(result)
        return self._me  # type: ignore

    async def log_out(self) -> bool:
        return await self.call("logOut")

    async def close_bot(self) -> bool:
        return await self.call("close")

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        *,
        parse_mode: str | None = None,
        entities: list[dict] | None = None,
        link_preview_options: dict | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        reply_parameters: dict | None = None,
        reply_markup: Any = None,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        **kwargs: Any,
    ) -> Message:
        data: dict[str, Any] = {"chat_id": chat_id, "text": text, **kwargs}
        if parse_mode:
            data["parse_mode"] = parse_mode
        if entities is not None:
            data["entities"] = entities
        if link_preview_options is not None:
            data["link_preview_options"] = link_preview_options
        if disable_notification is not None:
            data["disable_notification"] = disable_notification
        if protect_content is not None:
            data["protect_content"] = protect_content
        if reply_parameters is not None:
            data["reply_parameters"] = reply_parameters
        if business_connection_id:
            data["business_connection_id"] = business_connection_id
        if message_thread_id is not None:
            data["message_thread_id"] = message_thread_id
        if reply_markup is not None:
            data["reply_markup"] = reply_markup.to_dict() if hasattr(reply_markup, "to_dict") else reply_markup
        result = await self.call("sendMessage", data)
        return Message.from_dict(result)  # type: ignore

    async def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        **kwargs: Any,
    ) -> Message:
        data = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id, **kwargs}
        result = await self.call("forwardMessage", data)
        return Message.from_dict(result)  # type: ignore

    async def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        data = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id, **kwargs}
        return await self.call("copyMessage", data)

    async def send_photo(
        self,
        chat_id: int | str,
        photo: str | Path | BinaryIO,
        *,
        caption: str | None = None,
        parse_mode: str | None = None,
        reply_markup: Any = None,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendPhoto", chat_id, "photo", photo, caption=caption,
                                      parse_mode=parse_mode, reply_markup=reply_markup, **kwargs)

    async def send_audio(
        self,
        chat_id: int | str,
        audio: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendAudio", chat_id, "audio", audio, **kwargs)

    async def send_document(
        self,
        chat_id: int | str,
        document: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendDocument", chat_id, "document", document, **kwargs)

    async def send_video(
        self,
        chat_id: int | str,
        video: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendVideo", chat_id, "video", video, **kwargs)

    async def send_animation(
        self,
        chat_id: int | str,
        animation: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendAnimation", chat_id, "animation", animation, **kwargs)

    async def send_voice(
        self,
        chat_id: int | str,
        voice: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendVoice", chat_id, "voice", voice, **kwargs)

    async def send_video_note(
        self,
        chat_id: int | str,
        video_note: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        return await self._send_media("sendVideoNote", chat_id, "video_note", video_note, **kwargs)

    async def send_media_group(
        self,
        chat_id: int | str,
        media: list[dict[str, Any]],
        **kwargs: Any,
    ) -> list[Message]:
        data = {"chat_id": chat_id, "media": media, **kwargs}
        result = await self.call("sendMediaGroup", data)
        return [Message.from_dict(m) for m in result]  # type: ignore

    async def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        **kwargs: Any,
    ) -> Message:
        data = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude, **kwargs}
        result = await self.call("sendLocation", data)
        return Message.from_dict(result)  # type: ignore

    async def send_venue(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        **kwargs: Any,
    ) -> Message:
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
            **kwargs,
        }
        result = await self.call("sendVenue", data)
        return Message.from_dict(result)  # type: ignore

    async def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        **kwargs: Any,
    ) -> Message:
        data = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name,
            **kwargs,
        }
        result = await self.call("sendContact", data)
        return Message.from_dict(result)  # type: ignore

    async def send_poll(
        self,
        chat_id: int | str,
        question: str,
        options: list[str],
        **kwargs: Any,
    ) -> Message:
        data = {"chat_id": chat_id, "question": question, "options": options, **kwargs}
        result = await self.call("sendPoll", data)
        return Message.from_dict(result)  # type: ignore

    async def send_dice(self, chat_id: int | str, **kwargs: Any) -> Message:
        data = {"chat_id": chat_id, **kwargs}
        result = await self.call("sendDice", data)
        return Message.from_dict(result)  # type: ignore

    async def send_chat_action(self, chat_id: int | str, action: str, **kwargs: Any) -> bool:
        data = {"chat_id": chat_id, "action": action, **kwargs}
        return await self.call("sendChatAction", data)

    async def set_message_reaction(
        self,
        chat_id: int | str,
        message_id: int,
        reaction: list[dict] | None = None,
        **kwargs: Any,
    ) -> bool:
        data: dict[str, Any] = {"chat_id": chat_id, "message_id": message_id, **kwargs}
        if reaction is not None:
            data["reaction"] = reaction
        return await self.call("setMessageReaction", data)

    # ── Editing ──────────────────────────────────────────────────────

    async def edit_message_text(
        self,
        text: str,
        *,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: str | None = None,
        entities: list | None = None,
        reply_markup: Any = None,
        **kwargs: Any,
    ) -> Message | bool:
        data: dict[str, Any] = {"text": text, **kwargs}
        if chat_id is not None:
            data["chat_id"] = chat_id
        if message_id is not None:
            data["message_id"] = message_id
        if inline_message_id is not None:
            data["inline_message_id"] = inline_message_id
        if parse_mode:
            data["parse_mode"] = parse_mode
        if entities is not None:
            data["entities"] = entities
        if reply_markup is not None:
            data["reply_markup"] = reply_markup.to_dict() if hasattr(reply_markup, "to_dict") else reply_markup
        result = await self.call("editMessageText", data)
        if isinstance(result, dict) and "message_id" in result:
            return Message.from_dict(result)  # type: ignore
        return result

    async def edit_message_caption(
        self,
        *,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        caption: str | None = None,
        **kwargs: Any,
    ) -> Message | bool:
        data: dict[str, Any] = {**kwargs}
        if chat_id is not None:
            data["chat_id"] = chat_id
        if message_id is not None:
            data["message_id"] = message_id
        if inline_message_id is not None:
            data["inline_message_id"] = inline_message_id
        if caption is not None:
            data["caption"] = caption
        result = await self.call("editMessageCaption", data)
        if isinstance(result, dict) and "message_id" in result:
            return Message.from_dict(result)  # type: ignore
        return result

    async def edit_message_reply_markup(
        self,
        *,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: Any = None,
        **kwargs: Any,
    ) -> Message | bool:
        data: dict[str, Any] = {**kwargs}
        if chat_id is not None:
            data["chat_id"] = chat_id
        if message_id is not None:
            data["message_id"] = message_id
        if inline_message_id is not None:
            data["inline_message_id"] = inline_message_id
        if reply_markup is not None:
            data["reply_markup"] = reply_markup.to_dict() if hasattr(reply_markup, "to_dict") else reply_markup
        result = await self.call("editMessageReplyMarkup", data)
        if isinstance(result, dict) and "message_id" in result:
            return Message.from_dict(result)  # type: ignore
        return result

    async def delete_message(self, chat_id: int | str, message_id: int) -> bool:
        return await self.call("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

    async def delete_messages(self, chat_id: int | str, message_ids: list[int]) -> bool:
        return await self.call("deleteMessages", {"chat_id": chat_id, "message_ids": message_ids})

    # ── Callbacks ────────────────────────────────────────────────────

    async def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> bool:
        data: dict[str, Any] = {"callback_query_id": callback_query_id}
        if text is not None:
            data["text"] = text
        if show_alert is not None:
            data["show_alert"] = show_alert
        if url is not None:
            data["url"] = url
        if cache_time is not None:
            data["cache_time"] = cache_time
        return await self.call("answerCallbackQuery", data)

    # ── Inline ───────────────────────────────────────────────────────

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[dict[str, Any]],
        **kwargs: Any,
    ) -> bool:
        data = {"inline_query_id": inline_query_id, "results": results, **kwargs}
        return await self.call("answerInlineQuery", data)

    # ── Bot commands ─────────────────────────────────────────────────

    async def set_my_commands(self, commands: list[dict[str, str]], **kwargs: Any) -> bool:
        return await self.call("setMyCommands", {"commands": commands, **kwargs})

    async def delete_my_commands(self, **kwargs: Any) -> bool:
        return await self.call("deleteMyCommands", kwargs or None)

    async def get_my_commands(self, **kwargs: Any) -> list[dict[str, str]]:
        return await self.call("getMyCommands", kwargs or None)

    # ── Chat management ──────────────────────────────────────────────

    async def ban_chat_member(self, chat_id: int | str, user_id: int, **kwargs: Any) -> bool:
        return await self.call("banChatMember", {"chat_id": chat_id, "user_id": user_id, **kwargs})

    async def unban_chat_member(self, chat_id: int | str, user_id: int, **kwargs: Any) -> bool:
        return await self.call("unbanChatMember", {"chat_id": chat_id, "user_id": user_id, **kwargs})

    async def restrict_chat_member(
        self, chat_id: int | str, user_id: int, permissions: dict, **kwargs: Any
    ) -> bool:
        return await self.call(
            "restrictChatMember",
            {"chat_id": chat_id, "user_id": user_id, "permissions": permissions, **kwargs},
        )

    async def promote_chat_member(self, chat_id: int | str, user_id: int, **kwargs: Any) -> bool:
        return await self.call("promoteChatMember", {"chat_id": chat_id, "user_id": user_id, **kwargs})

    async def set_chat_title(self, chat_id: int | str, title: str) -> bool:
        return await self.call("setChatTitle", {"chat_id": chat_id, "title": title})

    async def set_chat_description(self, chat_id: int | str, description: str) -> bool:
        return await self.call("setChatDescription", {"chat_id": chat_id, "description": description})

    async def leave_chat(self, chat_id: int | str) -> bool:
        return await self.call("leaveChat", {"chat_id": chat_id})

    async def get_chat(self, chat_id: int | str) -> dict[str, Any]:
        return await self.call("getChat", {"chat_id": chat_id})

    async def get_chat_administrators(self, chat_id: int | str) -> list[dict]:
        return await self.call("getChatAdministrators", {"chat_id": chat_id})

    async def get_chat_member_count(self, chat_id: int | str) -> int:
        return await self.call("getChatMemberCount", {"chat_id": chat_id})

    async def get_chat_member(self, chat_id: int | str, user_id: int) -> dict:
        return await self.call("getChatMember", {"chat_id": chat_id, "user_id": user_id})

    # ── Files ────────────────────────────────────────────────────────

    async def get_file(self, file_id: str) -> File:
        result = await self.call("getFile", {"file_id": file_id})
        return File.from_dict(result)

    async def download_file(self, file_path: str) -> bytes:
        return await self.transport.download_file(file_path)

    # ── Payments / Stars ─────────────────────────────────────────────

    async def send_invoice(
        self,
        chat_id: int | str,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[dict],
        **kwargs: Any,
    ) -> Message:
        data = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": payload,
            "currency": currency,
            "prices": prices,
            **kwargs,
        }
        result = await self.call("sendInvoice", data)
        return Message.from_dict(result)  # type: ignore

    async def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[dict],
        **kwargs: Any,
    ) -> str:
        data = {
            "title": title,
            "description": description,
            "payload": payload,
            "currency": currency,
            "prices": prices,
            **kwargs,
        }
        return await self.call("createInvoiceLink", data)

    async def answer_pre_checkout_query(
        self, pre_checkout_query_id: str, ok: bool, **kwargs: Any
    ) -> bool:
        data = {"pre_checkout_query_id": pre_checkout_query_id, "ok": ok, **kwargs}
        return await self.call("answerPreCheckoutQuery", data)

    async def refund_star_payment(self, user_id: int, telegram_payment_charge_id: str) -> bool:
        return await self.call(
            "refundStarPayment",
            {"user_id": user_id, "telegram_payment_charge_id": telegram_payment_charge_id},
        )

    # ── Stickers ─────────────────────────────────────────────────────

    async def send_sticker(self, chat_id: int | str, sticker: str | Path | BinaryIO, **kwargs: Any) -> Message:
        return await self._send_media("sendSticker", chat_id, "sticker", sticker, **kwargs)

    # ── Forum / Topics ───────────────────────────────────────────────

    async def create_forum_topic(self, chat_id: int | str, name: str, **kwargs: Any) -> dict:
        return await self.call("createForumTopic", {"chat_id": chat_id, "name": name, **kwargs})

    async def edit_forum_topic(self, chat_id: int | str, message_thread_id: int, **kwargs: Any) -> bool:
        return await self.call(
            "editForumTopic",
            {"chat_id": chat_id, "message_thread_id": message_thread_id, **kwargs},
        )

    async def close_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        return await self.call(
            "closeForumTopic",
            {"chat_id": chat_id, "message_thread_id": message_thread_id},
        )

    async def reopen_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        return await self.call(
            "reopenForumTopic",
            {"chat_id": chat_id, "message_thread_id": message_thread_id},
        )

    async def delete_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        return await self.call(
            "deleteForumTopic",
            {"chat_id": chat_id, "message_thread_id": message_thread_id},
        )

    # ── Rich messages (Bot API 10.1+) ────────────────────────────────

    async def send_rich_message(
        self,
        chat_id: int | str,
        rich_message: Any,
        **kwargs: Any,
    ) -> Message:
        blocks = rich_message.to_list() if hasattr(rich_message, "to_list") else rich_message
        data = {"chat_id": chat_id, "rich_message": blocks, **kwargs}
        result = await self.call("sendRichMessage", data)
        return Message.from_dict(result)  # type: ignore

    # ── Internal helpers ─────────────────────────────────────────────

    async def _send_media(
        self,
        method: str,
        chat_id: int | str,
        field: str,
        media: str | Path | BinaryIO,
        **kwargs: Any,
    ) -> Message:
        data: dict[str, Any] = {"chat_id": chat_id, **kwargs}
        reply_markup = data.pop("reply_markup", None)
        if reply_markup is not None:
            data["reply_markup"] = reply_markup.to_dict() if hasattr(reply_markup, "to_dict") else reply_markup

        if isinstance(media, (str, Path)) and not str(media).startswith(("http://", "https://", "attach://")):
            path = Path(media)
            if path.is_file():
                with path.open("rb") as f:
                    files = {field: (path.name, f, "application/octet-stream")}
                    result = await self.transport.request(method, data, files=files)
            else:
                # Treat as file_id
                data[field] = str(media)
                result = await self.call(method, data)
        elif hasattr(media, "read"):
            files = {field: ("file", media, "application/octet-stream")}
            result = await self.transport.request(method, data, files=files)
        else:
            data[field] = media
            result = await self.call(method, data)
        return Message.from_dict(result)  # type: ignore
