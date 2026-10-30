# Custom Emoji

```python
from atlib.emoji import CustomEmoji, build_entities

text, entities = build_entities([
    "Reaction: ",
    CustomEmoji("🔥", "5368324170671202286"),
])
await bot.send_message(chat_id, text, entities=entities)
```

Requires a valid `custom_emoji_id` from Telegram. A plain Unicode emoji wrapped in `CustomEmoji` does **not** become a Premium emoji.
