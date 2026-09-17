---
id: engine-account-state
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Account state: one file per account, verdicts stacked

Optional. When the source is per-account (an account agent, a CRM with activity), the sweep keeps `overlay/accounts/<slug>/state.md`. It is operational (real names, never leaves the overlay). The operator reads one file per account and needs the delta since last time, not a recap. **The tenth run is better than the first only because it inherits the previous nine**, so verdicts stack and are never deleted.

## Cross-stream reconciliation

Hold two models of every active person. **Stated**: what they say in email, chat, meetings. **Revealed**: what product activity shows they do. Report the delta. Agreement between the two is unremarkable. When they conflict, revealed wins; chat is written for an audience, usage is not.

Patterns worth naming: "rolling out team-wide" plus few active seats is no internal buy-in. A blocked integration plus an active champion means they are carrying friction for you. **Chat warm plus activity flat is politeness, and it is the dangerous one.** A transcript names a need and no matching activity follows means they did not do the thing they said they needed.

## Epistemic discipline

Label every claim. **FACT** cites the event and timestamp. **INFERENCE** carries a confidence band. **ALTERNATIVE** is considered before inferring, not after. Three points and a story connecting them feels like insight and is usually noise.

When a tool fails or a field is unreachable, record it under data gaps and move on. A commitment that looks missed may have been kept somewhere the source cannot see; say so.

## Shape

```markdown
# <Account>, state as of YYYY-MM-DD HH:MM UTC (<tier>, <Nth> pull: <one-line headline>)

## Verdict
The finding this run, up front, FACT / INFERENCE / ALTERNATIVE labelled. Ends with "Net:" and what to do or watch.

## Verdict, prior (<date>, <Nth> pull: <headline>)
Stacked, newest first, never deleted.

## People
| Name | Role | Standing (champion / blocker / dormant) | Last real exchange |

## Open threads
Numbered. Whose court (you / them). Any dated promise.

## Friction
## Watch
Carried forward explicitly; resolve or re-carry each run.
## Changed since last run
## Data gaps
```

## Promote, don't bury

A pattern about the *operator* rather than the account, a product gap, or a source-wide tool behaviour does not belong here. Say "worth naming as a pattern" so the sweep's scan catches it, and queue it (`engine.py queue add --kind method` or `--kind new-situation`). The third instance of any manual hand-touch is a product ticket, not a task.

## Rules

"Nothing changed" is a valid and useful verdict. Name whose court the ball is in. Never invent activity or research. No customer-facing action from here; the sweep holds drafts, the operator sends.
