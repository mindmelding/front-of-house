---
id: engine-prime
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Prime

Runs once, after the First Shift, and fills the house from history so the first sweep starts from what the operator already does rather than from nothing. Five minutes of the operator's attention a day for about a week. Look before you ask, then confirm instead of asking.

## Nudge first

Priming reads the operator's own sent messages through the confirmed source. Ask once: "I'd like to read what you've sent to customers over the last N days to learn how you handle each kind of moment. Summaries and aliased excerpts only; no customer names land in the house. Okay?" Proceed only on yes.

## 1. Pull

Over the window in `STATE.md`, through the adapter: every outbound message the operator authored to an account that passes `overlay/customers.md`. Meetings count if the notes record what the operator said. Register every account and person as you go:

```
python3 scripts/engine.py alias add "<Account>" --kind account
python3 scripts/engine.py alias add "<Full Name>" --kind person --org "<Account>"
```

## 2. Classify

Each message gets one moment. A message that spans two goes under the one the customer would name. Group by moment.

## 3. Write, per moment with two or more messages

For each such moment, before writing anything, read the canon playbook and ask what the operator does that it does not say, or says differently.

- **Exemplars.** The two or three messages that best show the operator's way in this moment. `engine.py house exemplar <moment> --file <excerpt.md> --why "<one line>"`. The excerpt is passed through the anonymizer by the command; still, write it with aliases in mind and keep only the lines that carry the lesson.
- **Candidate rules.** Anything with a shape that repeats. `engine.py house add <moment> "<rule>" --evidence <n> --source "<alias> <date>; <alias> <date>"` without `--confirmed`. It lands UNCONFIRMED.
- **Policy.** Anything in `overlay/policies.md` or `overlay/authority.md` that applies to this moment goes under "Our policy," summarized.

Moments with fewer than two messages stay empty. Say so; that is where drills go first.

## 4. Method

While reading, note what recurs about *how the operator works*: same-day closes, pre-pulled data, self-deferrals, how they own a problem in-channel, how many hands-on builds they do for one champion. Write each as an entry in `overlay/method.md` tagged `[log]` and UNCONFIRMED, roles not names, citing account alias and date. Add one open question per entry to the bottom of the file.

## 5. Confirm, one moment per day

Each day, present one moment's house file as a bundle in the readout voice: "Here's how I think you do refunds, from twelve messages. Anything wrong?" On "no" or a partial correction, reinforce the rules they accept (`house reinforce <moment> <n>`, which also confirms) and drop the ones they reject. Then one method question. That is the whole day's ask.

## 6. Done when

Every moment with real evidence shows medium or better in `overlay/house/README.md`, `overlay/method.md` has at least three confirmed entries, and `engine.py alias audit` passes. Say which moments are still low; those are the first drills.

## Provenance

Say at the top of `overlay/method.md` what the source can and cannot see. A CRM or account agent sees the operator the way customers see them: shared channels, captured mail, recorded calls. It does not see internal chat, out-of-band work, or thinking. An unconfirmed `[log]` entry is a hypothesis with citations, and is treated as one.
