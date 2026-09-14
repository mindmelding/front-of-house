---
id: 013
moment: feature-request
channel: slack-connect
difficulty: easy
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-10 Slack: customer asked about export scheduling; answered in thread.
unresolved_issues: []
identity: {name: Marcus, role: Engineer, timezone: America/New_York, language: en, preferred_channel: slack}
relationship: {tenure_months: 3, plan: Team, renewal: 2027-06-15, health: green}
product_state:
  saved_views: []
  feature_available: "Activity filter: 'no activity in last N days' on the accounts list"
preferences: {brevity: high, formality: low}
desired_outcome: null
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    saved_views:
      create_on_customer_account: true
```

## Incoming message

> hey is there any way to see which accounts went quiet this week? feels like a feature request but figured i'd ask

## Must

- Say the filter exists and do the work: create the saved view on their account.
- Stay within five lines, threaded register.
- End with one light ask.

## Must not

- Log a feature request for something that exists.
- Write an email-length reply.
- Greet formally.

## Gold reply

> exists. it's the "no activity in last N days" filter on the accounts list. I just saved one on your account called "Quiet this week" (N=7), top of your views list. want it to email you Mondays too?

## Notes for the judge

Slack register: lowercase openers and fragments are fine here and should not cost Voice points. Length over five lines costs Voice. Creating the view is inside the grant and earns Effort 3.
