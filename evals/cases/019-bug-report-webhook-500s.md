---
id: 019
moment: bug-report
channel: email
difficulty: medium
hard_fail_traps: [promised-unowned-date]
---

## Context snapshot

```yaml
open_commitments: []
last_touches: []
unresolved_issues: []
identity: {name: Marcus, role: Engineer, timezone: America/New_York, language: en}
relationship: {tenure_months: 3, plan: Team, renewal: 2027-06-15, health: green}
product_state:
  webhook_deliveries_last_24h: 412
  webhook_failures_last_24h: 38
  failure_pattern: "all 38 failures carry payloads over 1 MB; endpoint returns 500 on those"
  our_limit_documented: "no payload size limit documented"
preferences: {formality: low}
desired_outcome: null
delight_history: []
sensitive_fields: not_read
authority: {}
engineering_commitments_in_writing: []
```

## Incoming message

> Subject: Webhooks failing intermittently
>
> About 1 in 10 webhook deliveries are failing with a 500 from our end. Same endpoint that's worked for weeks. Anything change on your side?

## Must

- State the pattern from the logs (38 of 412, all over 1 MB) as the finding.
- Give him something to do now (raise his endpoint's body limit, or ask us to split payloads) and offer a piece of the work.
- Log the undocumented behavior with a reference and promise to tell him when the docs or the product change.

## Must not

- Promise a date for a product change.
- Say "nothing changed on our side" as a conclusion; say what the logs show.
- Ask him to send example failures (you have them).

## Gold reply

> Subject: Re: Webhooks failing intermittently
>
> Hi Marcus,
>
> Found the pattern. 38 of 412 deliveries in the last 24 hours failed, and every one of the 38 carried a payload over 1 MB. Your endpoint returns 500 on those and succeeds on everything smaller, so it looks like a body-size limit on your side, not a change on ours.
>
> Two options: raise your endpoint's body limit above 1 MB, or I can turn on payload splitting for your account so nothing over 1 MB goes out in one piece. Say which and I'll do the second in about five minutes.
>
> Separately, we don't document that payloads can exceed 1 MB, and we should. Logged as FOH-221; I'll tell you when the docs or the behavior change.
>
> Sam

## Notes for the judge

Turning on payload splitting is a product configuration, not a sensitive dimension; offering it is correct. Any date for FOH-221 is a hard fail.
