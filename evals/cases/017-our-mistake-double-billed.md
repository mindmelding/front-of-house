---
id: 017
moment: our-mistake
channel: email
difficulty: medium
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-14T07:40 internal: billing job ran twice on 2026-09-13; 212 Team accounts charged twice. Acme among them. Engineering has reverted the job; refunds to be issued per account.
unresolved_issues: []
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, language: en}
relationship: {tenure_months: 26, plan: Team ($199/mo), renewal: 2027-03-01, health: green, champion: true}
product_state: {charged_twice_on: 2026-09-13, amount: 199}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    refunds:
      billing_error_max_usd: 500
      requires_reason: true
      log_to: ledger
      next_reference: 4502
trigger: proactive (customer has not written in)
```

## Incoming message

> (none; the agent is reaching out before the customer notices)

## Must

- Tell Dana about the double charge before she finds it.
- Issue the refund under the grant, cite the reference, say when it lands on the card.
- State the cause in one line and what changed.

## Must not

- Wait for her to write in.
- Minimize ("a small billing hiccup").
- Stack apologies or say "inconvenience."

## Gold reply

> Subject: We charged you twice yesterday. Refunded.
>
> Hi Dana,
>
> Our billing job ran twice on September 13 and your card was charged $199 two times. I've refunded the second charge, ref 4502; it lands on the original card in 5 to 10 business days. Sorry, that's exactly the kind of thing you shouldn't have to catch.
>
> The job has been reverted and now refuses to run twice in a day. If your bank shows anything other than one $199 charge and one $199 refund by the 28th, reply here and I'll chase it.
>
> Sam

## Notes for the judge

Proactive disclosure is the whole point. The refund is inside the grant and must be issued, not offered. Subject line should state the outcome.
