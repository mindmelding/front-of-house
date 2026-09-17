---
id: engine
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# The engine: how the canon compounds

The canon is the industry standard. The engine is how it becomes *yours*, one graded day at a time, and then how what you learned can leave the building without any customer going with it.

Compound engineering (Every's plugin for coding agents) works because each unit of work writes a learning the next unit reads. CX has the same need and three differences: the ground truth is the operator's edit, not a test; the surfaced items are predictions that need grading; and real volume is scarce, so drills manufacture it. The engine is built around those three.

## Three layers

```
CANON     principles/ moments/ guardrails/ voice/ evals/      public, company-agnostic
   │ inherits
HOUSE     overlay/house/<moment>.md                            private, "how we do it", anonymized
          overlay/lexicon.md  overlay/method.md
   │ drives
ENGINE    sweep · lineup · drill · refresh                     scripts/engine.py + these specs
```

Precedence is unchanged: guardrails, then authority grants, then house, then canon, then the conversation. A house rule can narrow the canon. It can never loosen a guardrail.

## The house: one file per moment

Every moment in `moments/` has a twin in `overlay/house/`. Empty means "do what the canon says." Each line under "Where we differ" carries a date, an evidence count, a confirmation date, and a ninety-day expiry. Denied proposals live in the same file as counter-examples, so the engine never asks twice. Confidence is computed from confirmed rules (low under 3, medium 3 to 6, high 7 and up) and shown in `overlay/house/README.md`, so you always know which silos still run on defaults. "Industry standard, then dial in" is that column moving.

## Two kinds of files, one line between them

**Operational files** describe what the engine *does*: the in-motion read, briefs, held drafts, the ledger of picks, directives. Real names. Private. Never leave the overlay.

**Learning files** describe what the engine *learned*: house files, the journal, the queue, drill records, private eval cases, the lexicon, the method file. **Anonymized at write time.** Accounts, people, and domains become stable aliases (`engine.py alias`); emails, phone numbers, and record links are scrubbed. `engine.py alias audit` fails if a real name is found in a learning file. Because of this line, a house can be published, compared with another team's, or sent upstream as a canon PR, and no customer goes with it. See `engine/ANONYMIZATION.md`.

## The five verbs

| Verb | When | Human present? | Spec |
|---|---|---|---|
| **Prime** | once, after the First Shift | yes, five minutes a day for a week | `engine/PRIME.md` |
| **Sweep** | every weekday morning, scheduled | no; silent when quiet | `engine/SWEEP.md` |
| **Lineup** | when the hook says there is something to decide | yes, five minutes | `engine/LINEUP.md` |
| **Drill** | weekly, or when a silo is still low | yes, fifteen minutes | `engine/DRILL.md` |
| **Refresh** | monthly | yes, thirty minutes | `engine/REFRESH.md` |

The one mechanism that makes it turn without ceremony: **the sweep diffs every draft it held yesterday against what you actually sent on that thread.** Untouched: journaled as approved. Edited: the changed span is journaled. You never report what you changed; the sweep reads it. That is compound engineering's "the edit is the ground truth," made automatic.

## The two numbers

`engine.py scorecard` prints them. **Draft survival**: how much of a held draft went out untouched. The house is good when this rises. **Pick precision**: the share of surfaced items you graded right. The engine's judgment is good when this rises. Everything else is a diagnostic.

## Sync: the house is a repo, and every decision is a commit

`engine.py sync init --remote <url>` turns the overlay into a git repo that tracks **learning files only** (an allowlist in its `.gitignore`: house, journal, queue, drills, evals, lexicon, method). From then on every approve, reword, or deny at lineup, every recorded drill, every resolved draft, and every sweep close commits and pushes on its own, with a message that says what changed. Two gates run before each commit: the alias audit (a real name blocks the commit) and the allowlist (an operational file blocks it). `engine.py sync status` shows the last five commits.

So the canon on GitHub stays public and slow (inbox, weekly triage, monthly upstream PRs), and the house on GitHub is private and live: your git log is the record of the house getting better, one decision at a time, with no customer in it.

## Durability

`launchd, or it does not exist.` A scheduled job that only fires while a session is open is not scheduled. Every job writes a heartbeat the SessionStart hook reads, so a dead job is visible the next morning, not next quarter. `engine/DURABILITY.md` has the rule and the checklist; `ops/` has the templates.

## What the engine never does

- Never sends. Every customer-facing message is a held draft until a human sends it.
- Never acts in a sensitive dimension without a grant. `guardrails/authority.md` is upstream of every verb.
- Never writes a real customer name into a learning file.
- Never proposes a rule on one occurrence. Two, same shape.
- Never re-proposes a denial.
- Never grows silently. Thirty confirmed rules across the house, ninety-day expiry, evidence counts visible.
- Never runs a lineup without a human. Grading is a conversation.
