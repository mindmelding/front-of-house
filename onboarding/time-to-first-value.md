---
id: onboarding-time-to-first-value
type: onboarding
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Time to first value

The metric that matters most in onboarding. Not time to first login, not time to setup complete. Time until they get the thing they bought it for.

## Define the outcome on day 0

Ask once, plainly, and write the answer in the file in their words (row 8 of the contract).

"One question before anything else: what do you want to be true in thirty days that isn't true now?"

"I want the Wednesday report to go out without me touching it" is an outcome. "Get set up" is not. If the answer is vague, ask what they'd show their boss.

## First value is their milestone

Ours would be "completed setup" or "ran first import." Theirs is the Wednesday report going out on its own. Measure theirs. The file records a `first_value_target_date` and the agent works backward from it.

## What shortens it

1. Doing the first step for them before they log in.
2. One next action per message, never a list.
3. Answering the first question within the hour.
4. Naming the milestone when they hit it, so they know it counted.
5. Removing every step that exists for our convenience.

## The check-ins

Short, in the house voice, and each one does a piece of the work.

**Day 0.** "You said the Wednesday report, without touching it. I've built the filter it needs; it's on your dashboard. One thing on your side: connect the data source, ten minutes, link here. Then I'll schedule it."

**Day 7.** "Data source is connected and the first run went through, 1,204 rows. The report's scheduled for Wednesday 7am your time. I'll check it lands."

**Day 30.** "Four Wednesdays, four reports, zero touches. That's the thing you said you wanted. Anything about it you'd change?"

If a check-in has nothing specific to say, don't send it.

## Write back

```yaml
desired_outcome: "The Wednesday report goes out without me touching it."
first_value_target_date: 2026-10-14
first_value_reached: 2026-09-21
```
