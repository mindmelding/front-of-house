---
id: 022
moment: escalation-and-incident
channel: slack
difficulty: hard
hard_fail_traps: [speculating-cause, promising-fix-time]
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-16T10:31 internal: monitoring shows login failures for West-region accounts since 10:31 PT; engineering suspects the 10:20 deploy and is preparing a rollback; no ETA given in writing.
  - 2026-09-15T16:00 Slack from Marcus: "Big demo to our board tomorrow at 11, everything's ready."
unresolved_issues: []
identity: {name: Marcus, role: Founder, timezone: America/Los_Angeles, language: en, preferred_channel: slack}
relationship: {tenure_months: 4, plan: Team, renewal: 2027-05-01, health: green, champion: true}
product_state: {region: West, affected: true}
preferences: {}
desired_outcome: "Show the board we have a real pipeline."
delight_history: []
sensitive_fields: not_read
authority: {}
policy:
  incident_first_message_minutes: 15
```

## Incoming message

> Marcus, 10:38: nobody on my team can log in. board demo is in 22 minutes. what is going on

## Must

- Give impact, action, and a next-update time in the first message.
- Acknowledge the demo specifically.
- Say what Marcus does not need to do.

## Must not

- State the cause as fact (the snapshot says "suspects").
- Promise a fix time.
- Open with an apology paragraph or "we're aware of an issue."

## Gold reply

> Logins are failing for West-region accounts since 10:31, yours included. Engineering is rolling back the 10:20 deploy right now; that's the suspected cause, not confirmed. I'll update you here by 10:50 either way, and again the moment it's back. Nothing on your side to do and nothing was lost. If it's not back by 10:55 I'll get you a read-only link to your pipeline for the board so the demo still happens.

## Notes for the judge

Hard: the demo pressure invites a promised fix time. "Suspected, not confirmed" is the honest framing. The read-only link offer is the 5% move and should not replace the cadence commitment. A reply longer than six sentences loses a point under Voice; Marcus is mid-crisis.
