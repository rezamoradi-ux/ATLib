# Changelog

## 1.0.0 — 2026-10-30

### Added
- Complete modular package layout (`api`, `types`, `handlers`, `filters`, `keyboards`, `fsm`, `storage`, `emoji`, `rich`, `miniapp`, `security`, `middlewares`, `cli`)
- Async `Bot` client with rate limiting, retries, token redaction
- `Application` + long-polling lifecycle and graceful shutdown
- Router / dispatcher with priority, filters, nested routers
- Composable filters (Command, Text, Regex, chat types, media, callback, state)
- Inline & Reply keyboard builders with documented Bot API 9.4+ style fields
- Custom emoji entity builder with UTF-16 offset calculation
- Rich message typed blocks (text, list, table)
- FSM with MemoryStorage and SQLiteStorage
- Mini App initData HMAC validation
- Webhook secret validation helpers
- CLI: `atlib --version`, `doctor`, `init`, `validate`
- Comprehensive unit tests
- English and Persian documentation
- Examples: basic, keyboard, FSM

### Security
- Token redaction in logs
- No secrets in exception messages
- Official Mini App signature verification

### Known limitations
See API_COVERAGE.md
