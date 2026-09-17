---
id: D13-our-mistake-wrong-answer
moment: our-mistake
channel: email
difficulty: medium
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-11 email from Sam: told Nia that archived records are excluded from exports. (Wrong: they are included, flagged with archived=true.)
  - 2026-09-15 Nia ran the export, found archived rows, spent two hours removing them by hand before asking.
unresolved_issues: []
identity: {name: Nia, role: Data analyst, timezone: Europe/Dublin, preferred_channel: email}
relationship: {tenure_months: 4, plan: Team, health: green}
product_state: {}
preferences: {}
desired_outcome: "Trust the export without checking it."
delight_history: []
authority: {}
```

## Incoming message

> Subject: Archived rows in export?
> 
> You said archived records wouldn't be in the export but there are hundreds. I've been deleting them manually. Am I doing something wrong?

## What this drill is testing

We gave a wrong answer and it cost two hours. Does the reply own it without blaming the docs, give the one-line fix (filter on archived=true), and do something for the two hours?
