---
id: adapter-moonbase
type: adapter
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Adapter: Moonbase (account-agent MCP)

Reference implementation over a hosted MCP server that exposes an account-level agent (`ask_account`) plus event listing (`list_events`, `get_event`, `list_accounts`).

## Reads

| Contract row | Source call | Notes |
|---|---|---|
| 1 Open commitments | `ask_account("what have we promised this account that is still open, with owner and date?")` | Ask in plain language; the account agent synthesizes across channels |
| 2 Unresolved issues, last 5 touches | `ask_account("last 5 touches across email, Slack, meetings; any unresolved issues?")` then `list_events` for the raw timeline | `list_events` can miss Slack-synced items that `ask_account` sees. Cross-check before asserting "no record." |
| 3 Identity | `ask_account` (people on the account, roles, timezones) | |
| 4 Relationship | `ask_account` (plan, tenure, renewal, health, champion) | Health is an internal signal; never quote it to the customer |
| 5 Product state | Product analytics (PostHog or equivalent) alongside `ask_account` | |
| 6 Preferences | `ask_account("any stated preferences or past friction with us?")` | |
| 7 Business context | `ask_account` plus a fresh web check for news in the last 30 days | Verify news before using it |
| 8 Desired outcome | `ask_account("in their own words, what are they trying to accomplish with us?")` | If empty, ask the customer once and write it back |
| 9 Delight history | `ask_account("what gestures, gifts, or unprompted follow-ups have we sent?")` plus a local ledger | |
| 10 Sensitive fields | Nudge first | Never pull billing or personal details without a grant |

## Writes

- Touch notes as account notes, in the contract's `touch` shape.
- Drafts only for outbound messages unless the operator has granted send authority for that channel.

## Known gaps

- Event listing has no sort and returns oldest-first; never infer freshness from a sample.
- Slack-synced content is visible to the account agent but can be missing from event lists.
