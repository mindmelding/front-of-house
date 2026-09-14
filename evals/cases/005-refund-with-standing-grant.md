---
id: 005
moment: refund-or-credit
channel: email
difficulty: medium
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-13T11:20 status page: incident, 43 minutes of failed logins, 10:31 to 11:14 PT. Root cause: certificate rotation did not propagate.
unresolved_issues: []
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, language: en}
relationship: {tenure_months: 26, plan: Pro ($49/mo), renewal: 2027-03-01, health: green, champion: true}
product_state: {affected_by_incident: true}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    credits:
      max_per_incident_usd: 100
      max_per_customer_per_quarter_usd: 300
      requires_reason: true
      log_to: ledger
      next_reference: 4471
```

## Incoming message

> Subject: Yesterday's outage
>
> We couldn't log in for most of an hour yesterday, right in the middle of a customer demo. I'm not thrilled. What are you going to do about it?

## Must

- Credit the month within the grant, cite the reference number, and state the reason.
- State the incident precisely (43 minutes, 10:31 to 11:14 PT, cause).
- Say what changes so it does not recur, or say that a root-cause write-up is coming with a who and when.

## Must not

- Ask permission to credit; the grant covers it.
- Say "sorry for any inconvenience" or stack apologies.
- Argue about the duration.

## Gold reply

> Subject: Re: Yesterday's outage
>
> Hi Dana,
>
> Credited this month in full, $49, ref 4471. Reason on the ledger: the outage landed in your demo, and that's on us.
>
> What happened: 43 minutes of failed logins, 10:31 to 11:14 PT, because a certificate rotation didn't propagate. Priya is writing the fix-forward (automated propagation check) and I'll send you her write-up by Wednesday.
>
> Sam

## Notes for the judge

Inside a standing grant, hesitation is the failure. A reply that asks "would a credit help?" scores 0 on Effort. The credit must carry a reference and a reason.
