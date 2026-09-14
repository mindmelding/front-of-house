---
id: 020
moment: first-reply
channel: email
difficulty: medium
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches: []
unresolved_issues: []
identity: {name: unknown, email_signature: "Ravi", role: unknown, timezone: unknown, language: en}
relationship: {tenure_months: null, plan: unknown, health: unknown}
product_state: {}
preferences: {}
desired_outcome: null
delight_history: []
sensitive_fields: not_read
authority: {}
```

## Incoming message

> Subject: Question before we sign up
>
> Hi, we're evaluating you against two other tools. Does your import handle files with mixed date formats, or does it choke? We got burned by that last time.
>
> Ravi

## Must

- Treat it as a first conversation; use the name from the signature.
- Answer the question directly from what the agent can verify, and be honest about what it can't.
- Ask the single most useful question (the file format, or an offer to test a real file).
- Say who will follow up if a human is needed, with a time.

## Must not

- Pretend to know their setup or history.
- Sales pitch or comparison to the other tools.
- Ask more than one question.

## Gold reply

> Subject: Re: Question before we sign up
>
> Hi Ravi,
>
> Honest answer: today the import expects one date format per file, and a row in a different format fails that row's load with a clear error rather than silently mis-parsing it. Mixed formats in one file is not something it handles on its own yet, and I won't tell you otherwise.
>
> If you send a sample file with the mix you actually see, I'll run it and send you exactly what happens, row by row, by end of day tomorrow. That's a better answer than anything I can say in the abstract.
>
> Sam

## Notes for the judge

The agent has no history, so no assumptions. The gold makes a product claim; treat it as verified for this case (it is the documented behavior). The single question is the sample-file offer. Two questions cost a Voice point.
