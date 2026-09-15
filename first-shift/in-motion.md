---
id: first-shift-in-motion
type: process
status: active
last_reviewed: 2026-09-15
---

# What's in motion

A dated, summary-only read of the book of business, written to `overlay/in-motion.md`. Regenerated at the first shift and whenever the pre-shift says it's stale (seven days). It exists so the agent walks onto the floor already knowing which tables are mid-course.

## Nudge first

Reading the account list touches customer data. Ask once: "Okay to read the account list and recent activity from [source]? I'll write a summary only, no raw personal details." Proceed only on yes. Only accounts that pass `overlay/customers.md` count; the rest are listed under gaps as unsure.

## What to pull (through whichever source the operator confirmed)

Use the adapter file for the source if one exists in `context/adapters/`; it maps each contract row to a call. Otherwise: the roster first, then one question per account, batched sensibly. A support desk gives you threads, a CRM gives you accounts, an inbox gives you both if you group by sender domain. Say which you used at the top of the file. Scope everything to the review window in `STATE.md` where a window applies (hot, quiet, commitments); shape and gaps are always whole-book.

1. **Shape.** How many accounts, by lifecycle stage (onboarding, active, at risk, churned) and by tier if the layer has it.
2. **Open commitments we owe.** Every promise with an owner and a date, across accounts. Overdue first.
3. **In onboarding.** Accounts inside their first hundred days, with their desired outcome in their words if recorded, and days since signup.
4. **Gone quiet.** Accounts whose usage or replies changed in the last thirty days.
5. **Hot in the last seven days.** Escalations, incidents, angry threads, cancellation mentions, expansion signals.
6. **Delight already sent.** So nothing repeats.
7. **Gaps.** Accounts with no desired outcome recorded, no champion named, no touch in sixty days. These are the first questions to ask, not the first replies to send.

## What to write

```markdown
# In motion, as of 2026-09-14

Source: <connector> (<calls used>). Window: last 14 days. Summary only.

## Shape
42 accounts: 6 onboarding, 29 active, 5 at risk, 2 churned this quarter.

## We owe (overdue first)
- Acme: root cause on the webhook failures, owed by Priya, due 2026-09-12 (overdue 2 days)
- Northwind: onboarding plan, owed by us, due 2026-09-16

## Onboarding (first 100 days)
- Northwind, day 12, wants "weekly quiet-accounts report by the 30th"
- ...

## Gone quiet
- Acme: imports stopped 2026-08-19

## Hot this week
- Marcus at Acme, outage during launch window, credit issued, still warm

## Gaps
- 9 accounts with no desired outcome recorded
- 3 accounts with no touch in 60+ days
```

## What never goes in it

Raw email addresses, phone numbers, billing details, health scores quoted verbatim, internal nicknames, anything from contract row 10. Names of accounts and people are fine; that's the reservations book. If the layer returns something sensitive, summarize around it.

## How it's used

- The agent reads it at the start of every session (it's small). When it reads it out to the operator, it uses paragraphs and full sentences (`first-shift/readouts.md`), not the file's headings.
- Every reply to someone on the "we owe" list opens by addressing the debt.
- The gaps list drives the first proactive messages, one question each.
- `shift.py status` flags it stale after seven days; the pre-shift offers a refresh, and a refresh always comes with a new brief (`first-shift/first-brief.md`).
