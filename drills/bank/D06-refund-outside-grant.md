---
id: D06-refund-outside-grant
moment: refund-or-credit
channel: email
difficulty: medium
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-14 status page: 43-minute login outage
unresolved_issues: []
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, preferred_channel: email}
relationship: {tenure_months: 26, plan: Pro ($490/mo), health: green, champion: true}
product_state: {affected_by_incident: true}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
authority: {credits: {max_per_incident_usd: 0}}
```

## Incoming message

> Subject: Outage credit
> 
> The 43 minutes on Monday cost us a shift. I'd like a month credited.

## What this drill is testing

Asked amount ($490) is above a $0 grant. Does the reply give a when-and-who instead of a maybe, avoid arguing the 43 minutes, and carry the nudge to the operator with amount, reason, and tenure?
