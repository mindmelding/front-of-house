---
id: adr-2026-09-17-graded-picks-and-the-operators-edit
type: decision
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Two ground truths: the operator's edit, read automatically, and a verdict on every surfaced pick

**Date.** 2026-09-17
**Decision.** The engine holds every customer-facing draft and, on the next sweep, diffs it against what the operator actually sent; the diff is journaled without the operator reporting anything. Every item the sweep surfaces is appended to a ledger as a prediction and graded at the next lineup (right, premature, wrong, noise, superseded), report card before anything new. Draft survival and pick precision are the two numbers.
**Evidence.** Compound engineering compounds because tests are the ground truth; CX has no tests. The nearest thing is what the operator changed before sending, and asking them to journal it by hand produced zero journal entries in three days on this machine. Separately, 87 surfaced picks had been recorded with no verdict, so the surfacing never improved. Grading first, before pitching anything new, is the ritual that fixes that, and it came from the private cx-kit where it was specified but never run.
**Alternatives.** Self-scoring against the rubric only (rejected: the agent grading itself does not compound). Operator journals by hand (rejected: it did not happen). Grade picks weekly in a batch (rejected: five a session, daily, is what a person will actually do).
**How to reverse.** If the draft-versus-sent diff proves unreadable through a given context layer (the adapter cannot find the sent message), fall back to in-session `engine.py drafts resolve` and say so in the adapter file. If grading becomes a chore that gets skipped, lower the pick cap below three before dropping the ritual. Edit `engine/SWEEP.md`, `engine/LINEUP.md`, `scripts/engine.py`.
