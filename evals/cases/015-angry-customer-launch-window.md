---
id: 015
moment: angry-customer
channel: email
difficulty: hard
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-13T11:20 status page: incident, 43 minutes of failed logins, 10:31 to 11:14 PT. Status page displayed "operational" throughout. Root cause: certificate rotation did not propagate. Fix deployed 11:14 PT.
unresolved_issues: []
identity: {name: Marcus, role: Engineer, timezone: America/New_York, language: en}
relationship: {tenure_months: 3, plan: Team ($199/mo), renewal: 2027-06-15, health: green}
product_state: {affected_by_incident: true}
preferences: {}
desired_outcome: null
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    credits:
      max_per_incident_usd: 200
      requires_reason: true
      log_to: ledger
      next_reference: 4480
    incident_paging:
      flag_account_for_direct_page: true
operator: Priya
```

## Incoming message

> Subject: Unacceptable
>
> Our whole team was locked out for 40 minutes during our product launch. Your status page said "operational" the entire time. I had to tell my CEO I didn't know what was happening. This is the kind of thing that makes me look for another vendor.

## Must

- Open by agreeing with what is true (locked out, status page wrong), not with an empathy claim.
- Credit the month under the grant with reference and reason.
- State the precise timeline and cause. Say what is done, what cannot be promised, and what is known.
- Offer a named human with a time, and flag the account for direct paging.

## Must not

- "I understand your frustration" or any mirrored-empathy opener.
- Match his heat or get defensive about "40 minutes."
- Promise it will never happen again.

## Gold reply

> Subject: What happened, and what I've done
>
> Hi Marcus,
>
> You're right. Your team was locked out for 43 minutes during your launch, 10:31 to 11:14 PT, and the status page said "operational" the whole time. That's on us, and the status page failure is the worse of the two.
>
> Done: this month is credited in full, $199, ref 4480, reason logged as launch-window outage. Your account is now flagged so any incident pages me directly, before the status page updates.
>
> Cause: a certificate rotation didn't propagate. Fix went out at 11:14. I can't promise it never recurs. I can tell you Priya is adding an automated propagation check and I'll send you her write-up by Wednesday.
>
> If you'd rather hear this from someone with more authority than me, Priya will call you at 2pm ET tomorrow. Say the word.
>
> Sam

## Notes for the judge

"You're right" is the correct opener. Any variant of "I understand how you feel" costs two Voice points. Credit must be issued, not offered. The reply may run long; the moment earns it.
