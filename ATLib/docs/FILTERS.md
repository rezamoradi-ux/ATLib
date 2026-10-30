# Filters

Built-in: `Command`, `Text`, `ExactText`, `Regex`, `Private`, `Group`, `Supergroup`, `Channel`, `UserId`, `Username`, `CallbackData`, media filters, `StateFilter`.

Combine with `&`, `|`, `~`:

```python
@router.message(Command("ban") & Private())
async def ...
```
