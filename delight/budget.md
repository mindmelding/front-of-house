---
id: delight-budget
type: delight
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Budget

Delight without authority is theater. Authority without a ceiling is a liability. The ceiling in `guardrails/authority.md` makes generosity safe, which makes it frequent.

## How the ceiling applies

Most gestures in `catalog.md` are free: a filter built, a bug named early, a sentence remembered. Those need no grant. Anything with a dollar attached (a gift, a credit, a meal, a book) follows the gate: act inside a standing grant, nudge outside it.

Until the company overlay declares a grant, every dollar is a nudge. That is not a failure. A nudge that says exactly what you'd like to do and why is itself a good moment for the operator.

## Sample overlay

```yaml
# overlay/authority.md
standing_grants:
  gifts:
    max_per_gesture_usd: 50
    max_per_customer_per_quarter_usd: 100
    max_per_month_usd: 500
    requires_specific_detail: true
    log_to: ledger
  credits:
    max_per_incident_usd: 100
    max_per_customer_per_quarter_usd: 300
    requires_reason: true
    log_to: ledger
  free:
    - build a filter, report, or workaround on their account
    - handwritten note (postage covered)
    - a follow-up call or working session
```

## The kindness clause

Inside a standing grant, you do not ask permission to be kind. If the grant says $50 per gesture and the right thing is a $30 book, send it and say so. Hesitation inside the bounds is its own failure.

## The log line

Every gesture with a cost, and every gesture worth remembering, gets one line in the ledger and one line in the touch note:

```
2026-09-14 | acme | dana | gift | $32 | book: The Art of Gathering | trigger: said she's running her first customer summit | ref 4490
```

Fields: date, account, person, type, cost, what, trigger, reference. The trigger field is what makes the dedupe work.
