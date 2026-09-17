---
id: drills
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Drills: the scenario bank

Scenarios ship without answers. The answers are your house.

Each file in `bank/` is one situation: a context snapshot in the shape of `context/CONTRACT.md`, the incoming message (or the trigger for an outbound), and one line on what the drill is testing. No gold reply. A team's first week on the canon is drilling these; their replies become their `overlay/house/<moment>.md` rules and their private eval cases, and the confidence column in `overlay/house/README.md` moves from low toward high. Industry standard, then dialed in.

The canon's `evals/cases/` double as drills; the engine hides the gold until the drill is recorded.

## Running one

`python3 scripts/engine.py drill next` picks three, lowest-confidence silo first. Then follow `engine/DRILL.md`: set the table, the operator answers (or edits your draft), score both against `evals/rubric.md`, name the delta, ask "what's the rule?", record it.

## Adding one

A new situation the sweep found and no moment covers is the best source (`overlay/drills/new-situations.md`, already anonymized). Shape it like the files here, one page, and open a PR. Every moment should have at least one; a moment with three or more is a moment the community has strong opinions about.

## Comparing houses

Because house files are anonymized at write time, two teams can drill the same scenario and compare rules without either seeing the other's customers. That comparison is the thing this bank exists for. A rule both teams reached independently is a candidate for the canon.
