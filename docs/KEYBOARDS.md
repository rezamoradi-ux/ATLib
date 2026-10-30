# Keyboards

```python
from atlib import InlineKeyboard, InlineButton

kb = InlineKeyboard()
kb.row(
    InlineButton("OK", callback_data="ok"),
    InlineButton("Site", url="https://example.com"),
)
# Optional style / icon fields (client-dependent rendering)
kb.row(InlineButton("Premium", callback_data="p", style="primary", icon_custom_emoji_id="ID"))
await ctx.answer("Choose:", reply_markup=kb)
```

Telegram decides final rendering; not all clients show `style` or custom emoji icons identically.
