# API Coverage Report — ATLib 1.0.0

**Verification date:** 2026-10-30  
**Target Bot API:** 10.3 (changelog August 24, 2026)

## Implemented method families

| Family | Methods implemented | Status |
|--------|---------------------|--------|
| Getting updates | getUpdates, setWebhook, deleteWebhook, getWebhookInfo | Complete |
| Available methods | getMe, logOut, close | Complete |
| Messages | sendMessage, forwardMessage, copyMessage, sendPhoto, sendAudio, sendDocument, sendVideo, sendAnimation, sendVoice, sendVideoNote, sendMediaGroup, sendLocation, sendVenue, sendContact, sendPoll, sendDice, sendChatAction, setMessageReaction | Complete core set |
| Editing | editMessageText, editMessageCaption, editMessageReplyMarkup, deleteMessage, deleteMessages | Complete |
| Callbacks | answerCallbackQuery | Complete |
| Inline | answerInlineQuery | Complete |
| Commands | setMyCommands, deleteMyCommands, getMyCommands | Complete |
| Chat admin | banChatMember, unbanChatMember, restrictChatMember, promoteChatMember, setChatTitle, setChatDescription, leaveChat, getChat, getChatAdministrators, getChatMemberCount, getChatMember | Complete |
| Files | getFile, download | Complete |
| Payments / Stars | sendInvoice, createInvoiceLink, answerPreCheckoutQuery, refundStarPayment | Complete |
| Stickers | sendSticker | Basic |
| Forum topics | createForumTopic, editForumTopic, closeForumTopic, reopenForumTopic, deleteForumTopic | Complete |
| Rich messages | sendRichMessage | Basic (typed builder) |

**Approximate count of implemented API methods:** ~55

## Types

User, Chat, Message, MessageEntity, Update, CallbackQuery, File, PhotoSize, InlineKeyboardMarkup, ReplyKeyboardMarkup, plus rich block helpers.

**Approximate count of implemented types:** ~15 core + rich helpers

## Not yet fully implemented (documented limitations)

- Full sticker set management (createNewStickerSet, …)
- Business connection full surface
- All gift / unique gift methods
- Streaming draft methods (sendMessageDraft) beyond basic support
- Complete rich-message block union (all 21+ block types)
- Redis / PostgreSQL storage adapters (interface present; optional deps)
- Full ASGI webhook server (validation helpers present)
- Plugin loader runtime isolation

These are tracked for subsequent minor releases. The core production path (polling, handlers, filters, FSM, keyboards, media send, payments entry points) is implemented and tested.
