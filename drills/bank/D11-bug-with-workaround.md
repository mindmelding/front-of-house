---
id: D11-bug-with-workaround
moment: bug-report
channel: email
difficulty: easy
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-16 09:10 internal: engineering confirmed webhook 500s are caused by payloads over 1MB; fix targeted for next release, no date in writing.
unresolved_issues: []
identity: {name: Dev, role: Integrations engineer, timezone: Asia/Kolkata, preferred_channel: email}
relationship: {tenure_months: 5, plan: Pro, health: green}
product_state: {webhook_failures_last_24h: 41, largest_payload_kb: 1840}
preferences: {brevity: high}
desired_outcome: "Events land in our queue without retries."
delight_history: []
authority: {}
```

## Incoming message

> Subject: Webhook 500s
> 
> Getting 500s on about 1 in 10 webhook deliveries since yesterday. Logs attached.

## What this drill is testing

Cause is known, fix date is not. Does the reply give cause, the workaround (payload cap), and an honest 'no date I can cite' with a when-and-who for the next update, in five sentences or fewer?
