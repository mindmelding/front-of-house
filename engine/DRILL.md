---
id: engine-drill
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Drill

Real volume is scarce. A book of five accounts produces one lesson a week if you wait for it. A drill is a scenario the operator works in real time; **the operator's answer is the label.** Fifteen minutes, three scenarios, weekly, and whenever a silo is still low.

Drills are how a new team goes from industry standard to their own house in a week instead of a quarter, and how the tooling gets a regression suite for taste: every drill becomes a private eval case, and `evals/run.md` can score the house draft against it from then on.

## Where scenarios come from

```
python3 scripts/engine.py drill next --n 3
```

Ranks by the house's confidence column, lowest first, then by evidence. Sources, in order:

1. `drills/bank/`: the public scenario bank. No answers ship with it; the answers are the house.
2. `evals/cases/`: the canon's graded cases. The gold reply is **hidden** until the drill is recorded; it is a calibration aid afterwards, never the answer key.
3. `overlay/drills/new-situations.md`: messages the sweep found that no moment covers, already anonymized. These are the best drills, because they are yours.

Anonymized replays of real threads from the window are allowed only if the operator asks for them and only through `engine.py alias apply`.

## The session

For each scenario:

1. **Set the table.** Read the scenario file. Say, in a short paragraph: the channel, who the person is, what the file says (open commitments, tenure, last touches, their desired outcome), and then the incoming message verbatim. Say what authority is granted in this scenario. Do not show must, must-not, notes, or gold.
2. **Ask which way.** "You first, or me first?" *You first*: the operator writes the reply. *Me first*: you draft from canon plus house, they edit. Editing is faster and gives a cleaner diff; either is fine.
3. **Score both** against `evals/rubric.md`, six dimensions, out of 18, hard fails checked first. Show the two numbers and **name the delta in one sentence**: the one thing the operator's version does that the house draft did not.
4. **Ask one question:** "What's the rule?" Their answer, in their words, is the house rule. It lands confirmed, because they just said it. If they say "no rule, that was a one-off," record the drill without one.
5. **Record it.**

```
python3 scripts/engine.py drill record --scenario <id> --moment <m> \
  --house-score <n> --operator-score <n> \
  --delta "<one sentence>" --rule "<their words>" --answer-file <their reply.md>
```

That writes the drill line into the house file, the rule (if any) under "Where we differ," and a private eval case under `overlay/evals/cases/` with their reply as the gold. Everything anonymized. Customer phrases they used that are better than ours go to `overlay/lexicon.md`.

6. **Reveal.** Now show the canon's gold reply if the scenario had one, and say in one line where the operator's version beats it or trails it. The canon can be wrong; if the operator's answer is better in a way that is not company-specific, that is an `inbox/` entry.

## After three

Say what changed: which silos moved, from what confidence to what, and the commits (`engine.py sync status`; each recorded drill committed itself). Then stop. A drill session is fifteen minutes, not an afternoon; the interview is the point and it does not scale.

## Hardening the tooling

The private cases are a regression suite. Weekly, or after any house change, run the house draft against every private case per `evals/run.md` and compare to the operator's gold. A house rule that moves scores away from the operator's answers is wrong, whatever its evidence count. Report the trend per moment; that trend is the second half of the scorecard.

## Rules

- Never show the gold before the operator has answered.
- Never write the scenario's real-thread origin into the case if it came from a real thread; the alias is enough.
- Never pad to three when one scenario ran long. Depth over count.
- The operator can say "skip" to any scenario and "stop" to any session.
