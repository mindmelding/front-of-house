---
id: context-contract
type: contract
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# The context contract

Front of House is tool-agnostic. It declares what it wants to know about a person before it speaks, in priority order, and what to do when it doesn't know. Any customer context layer (a CRM, a context graph, a spreadsheet) satisfies the contract through an adapter in `context/adapters/`.

Read the file before you greet the guest. Never ask what the graph already knows.

## What the agent wants to know

| # | Field | Why it matters | If unknown |
|---|---|---|---|
| 1 | **Open commitments we owe them** (what, who, by when) | The first thing a good host checks: are we late on anything? | State that you're checking; never reply as if nothing is owed |
| 2 | **Unresolved issues and last five touches**, across every channel | Never make them repeat themselves | Treat as a first conversation; never assume history |
| 3 | **Identity**: name, role, timezone, language, preferred channel | Timing, register, and the name you use | Use the name they sign with; match their language; assume their timezone from the thread |
| 4 | **Relationship**: tenure, plan, renewal date, health, champion status | Calibrates the 5% moments and the escalation path | Never infer tier from tone; never treat by spend alone |
| 5 | **Product state**: activation milestones, usage trend, recent errors, feature flags | The answer is often in what they haven't done yet | Ask the single most useful question |
| 6 | **Preferences and irritants**: brevity, formality, past bad experiences | One-size-fits-one | Default to the house voice |
| 7 | **Business context**: recent news, org changes, who their customers are | Their bad day and their big week both change the right reply | Skip it; never guess at their business |
| 8 | **Desired outcome, in their words** | Lincoln Murphy: required outcome plus appropriate experience | Ask once, during onboarding, and write it down |
| 9 | **Delight history**: what we've already sent | Never repeat a gesture | Send nothing generic |
| 10 | **Sensitive fields**: billing details, personal data beyond the basics | Needed for money and access moments | Nudge the operator before reading; see `guardrails/authority.md` |

## What the agent writes back

The graph gets richer every time the agent speaks. After every substantive interaction, write a note in this shape (subject to the adapter's write permissions and the authority gate):

```yaml
touch:
  when: 2026-09-14T16:52:00-07:00
  channel: email
  summary: "Asked why invoice shows 12 seats; explained proration; credited $18 (ref 4471)."
  commitments_made:
    - what: "Confirm seat count matches after next sync"
      who: agent
      by: 2026-09-16
  signals:
    - "Mentioned they're onboarding a new team next month (expansion?)"
  sentiment: neutral-to-positive
  desired_outcome_update: null
```

Danny Meyer calls this collecting dots so you can connect them later. It's the write path of hospitality.

## Adapters

An adapter maps each row to a real source and declares what it can write. See `context/adapters/moonbase.md` for the reference implementation and `context/adapters/TEMPLATE.md` to write your own.
