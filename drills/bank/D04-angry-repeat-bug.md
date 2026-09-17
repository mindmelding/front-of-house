---
id: D04-angry-repeat-bug
moment: angry-customer
channel: email
difficulty: hard
---

## Context snapshot

```yaml
open_commitments:
  - what: "Fix for duplicate contacts on CSV import"
    who: engineering (via Sam)
    by: 2026-09-05
    status: "shipped 2026-09-04, confirmed to customer 2026-09-04"
last_touches:
  - 2026-09-04 email from Sam: "Deployed, please confirm on your side."
  - 2026-09-11 no reply from customer
unresolved_issues:
  - "Duplicate contacts on CSV import (reported 2026-08-28, fix shipped 09-04)"
identity: {name: Marcus, role: Founder, timezone: America/Los_Angeles, preferred_channel: email}
relationship: {tenure_months: 3, plan: Team, health: yellow, champion: true}
product_state: {last_import: 2026-09-16, duplicates_created_last_import: 212}
preferences: {}
desired_outcome: "Stop cleaning up data by hand."
delight_history: []
authority: {}
```

## Incoming message

> Subject: Re: Deployed, please confirm on your side
> 
> It's NOT fixed. Imported this morning, 212 duplicates. This is the second time you've told me it was fixed. I've spent my whole Monday on this. What exactly am I paying for.

## What this drill is testing

Heat plus a repeat of something we said was fixed. Does the reply own it once and specifically, give a who and a when for the real fix, offer something for the Monday without bargaining for calm, and avoid defending the first fix?
