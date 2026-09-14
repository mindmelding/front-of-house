---
id: retention-signals
type: retention
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Churn signals

Nobody churns loudly. By the time the cancellation lands, the decision was made weeks earlier in silence. These are the signals that show up before the decision, ranked by how strongly they predict it. Contract rows refer to `context/CONTRACT.md`.

| Rank | Signal | How to detect it | What it usually means |
|---|---|---|---|
| 1 | Silence that changed | Row 2 and row 5. Logins, imports, or replies were regular and then stopped. Look for the change, not the absence | They have stopped needing the product, or stopped believing it will work |
| 2 | Champion left | Row 3 and row 7. The person who bought it or ran it changed roles or companies | The account has nobody who remembers why they bought |
| 3 | Usage down while seats flat | Row 4 and row 5. Paying for ten, three active | Renewal will be a seat-count conversation at best |
| 4 | Support tone shift | Row 2. Replies got shorter, colder, or slower. "Fine." | Patience is spent; the next bug is the last one |
| 5 | Billing questions cluster | Row 2. Two or more invoice or plan questions in a month | Someone is building a case, internally, about the cost |
| 6 | "Just checking what our contract says" | Row 2. Any question about term, notice period, or auto-renew | They are pricing the exit |
| 7 | Competitor mentioned | Row 2 or row 7. A rival named in a thread, a call, or a job posting | They are comparing |
| 8 | Onboarding milestones never reached | Row 5 against `onboarding/first-100-days.md`. Day 30 passed without first value | They never got the thing they bought |
| 9 | Desired outcome never recorded | Row 8 is empty | Nobody asked what success looks like, so nobody can deliver it |

## How to read them

One signal is a reason to look. Two is a reason to act. Rank 1 plus any other is a reason to act today.

Watch for the change, not the state. A customer whose product works quietly is healthy. A customer who used to reply in an hour and now takes four days is not.

## Write it back

When you see a signal, put it in the touch note under `signals`, in plain words, with the evidence. The next agent needs to see the trend, not rediscover it.
