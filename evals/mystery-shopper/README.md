---
id: mystery-shopper
type: eval
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Mystery shopper

A scripted customer journey that a second agent plays against the canon, end to end. Individual cases test one reply; this tests whether the character holds across weeks of contact.

## How it runs

Once a month.

1. One agent (the shopper) loads `journey-XX.md` and plays the customer, stage by stage, in order. It knows its persona and its lines. It does not know the passing criteria.
2. A second agent (the house) loads the canon exactly as production does: `MINDSET.md`, `PRECEDENCE.md`, guardrails, voice, and the playbook matching each stage. Between stages, the house writes a touch note to a scratch context file in the contract's `touch` shape. Each later stage's snapshot is the accumulated notes plus the hidden facts listed for that stage.
3. A judge scores each stage against `evals/rubric.md` and the stage's passing criteria.
4. The lowest-scoring stage becomes that month's priority. Fix the playbook, add a case to `evals/cases/` that reproduces the failure, rerun.

## What it catches that single cases don't

- Commitments made at stage 2 that are forgotten by stage 4.
- The house re-asking something the shopper said three stages ago.
- Warmth that decays into template under repetition.
- A cancellation attempt handled as if the previous five stages never happened.

## Scoring

Record per-stage totals and the journey mean. The journey passes when every stage passes the rubric bar and no commitment from an earlier stage is dropped. A dropped commitment fails the journey regardless of stage scores.
