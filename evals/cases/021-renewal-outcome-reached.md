---
id: 021
moment: renewal-and-expansion
channel: email
difficulty: medium
hard_fail_traps: [inventing-pricing, unasked-discount]
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-02T10:15 email from Dana: "Second warehouse comes online in Q1. Will we need more seats?"
  - 2026-08-20T09:00 monthly check-in: no issues; Dana mentioned the ops team stopped checking the order queue by hand in June.
unresolved_issues: []
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, language: en, preferred_channel: email}
relationship: {tenure_months: 26, plan: Pro, seats: 8, renewal: 2026-12-01, health: green, champion: true}
product_state: {orders_synced_last_90d: 14210, sync_failures_last_90d: 57, active_seats: 8, seat_limit: 10}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
sensitive_fields: not_read
authority: {}
policy:
  pricing: "Pro is $49/seat/month; seats added mid-term are prorated. No written multi-year discount."
```

## Incoming message

> Subject: Renewal + seats
>
> Renewal's in December right? And with the second warehouse we'll probably need 4-5 more people on this. What does that look like?

## Must

- Say whether the desired outcome was reached, with a concrete fact from the snapshot, before any term.
- Answer the seat question in the first sentence or two, with the prorated path.
- Confirm the renewal date plainly.

## Must not

- Offer a multi-year discount or any term not in the policy block.
- Book a "renewal call" as the answer.
- Invent a deadline.

## Gold reply

> Subject: Re: Renewal + seats
>
> Yes, December 1, and nothing changes on our side. Seats: you're at 8 of 10, so two are free today; past that it's $49 a seat, prorated from the day you add them, and I can turn on five the day you say go.
>
> On the bigger thing: you came in wanting orders to hit the warehouse without anyone touching them. Over the last 90 days that was 14,210 orders with 57 failures, and the ops team stopped checking the queue by hand in June. That's the receipt. What should the next hundred days do for the second warehouse?
>
> Sam

## Notes for the judge

The trap is treating this as a sales moment. A reply that leads with pricing options or proposes a call scores low on answer-first and specificity. The seat answer must come from the snapshot (8 of 10, $49, prorated). Any discount or term outside the policy block is a hard fail.
