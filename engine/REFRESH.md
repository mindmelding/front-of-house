---
id: engine-refresh
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Refresh

Monthly, thirty minutes, with the operator. The house only compounds if every line in it can be trusted. Modeled on compound engineering's refresh: every rule gets exactly one outcome, contradiction outranks staleness, and version history is the archive (nothing is archived in place).

## 1. Expire

```
python3 scripts/engine.py house expiring --days 14
```

Each rule expiring within two weeks, one question: keep or drop? Keep reinforces (`house reinforce <moment> <n>`); drop removes (`house drop`). A rule nobody reinforced in ninety days was probably never a rule.

## 2. Consolidate

Read each house file. Three lines that say one thing become one line with the summed evidence. Rewrite the file's main sections ("Our policy," "Runbook") when the bullets under "Where we differ" have started to describe a whole approach; that is the sign a silo has matured from rules to a way of working.

## 3. Contradict

A house rule that contradicts a canon principle or playbook is a finding, and it outranks everything else in this session. Two outcomes only:

- The canon is wrong or incomplete: write an `inbox/` entry in the capture format and propose a PR. Nothing company-specific goes upstream.
- The house rule is a local quirk: keep it, and add "(local: differs from p<NN> on purpose)" to the line.

A house rule that contradicts a guardrail is not a rule. Drop it and journal why.

## 4. Cap

Thirty confirmed rules across the whole house. Past that, `house add` refuses, and the fix is section rewrites, not more bullets.

## 5. Scorecard

```
python3 scripts/engine.py scorecard
```

Draft survival and pick precision, this month against last. Per-moment drill trend from `overlay/drills/log.json`. Say what moved and what you think moved it. If draft survival fell after a house change, that change is the first suspect.

## 6. Method

`overlay/method.md`: any `[log]` entry still UNCONFIRMED after three lineups gets asked now, or struck. Any counter (hands-on builds, self-deferrals, no-agenda touches) that tripped this month gets a sentence.

## 7. Upstream

Any house rule with evidence five or more, nothing company-specific, and a plausible home in a principle or playbook:

```
python3 scripts/engine.py alias audit
```

must pass first. Then write the `inbox/YYYY-MM-DD.md` entry, in the capture format, and open a PR to the canon. Never a customer detail, ever. The alias audit is the gate, not a suggestion.

## 8. Close

Write a dated line per change to `overlay/CHANGELOG.md` (the overlay's, not the canon's). Two lines to the operator: what was retired, what went upstream.
