# Security

- Never commit bot tokens. Use environment variables or a secrets manager.
- ATLib redacts tokens from log messages by default.
- Mini App `initData` must always be validated with `validate_init_data` before trusting user data.
- Webhook endpoints should verify the `X-Telegram-Bot-Api-Secret-Token` header.
- File downloads should validate paths; do not concatenate untrusted input into filesystem paths.
- Rate limiting and throttling middleware reduce abuse surface but do not replace application-level authorization.
