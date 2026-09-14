---
id: 001
moment: first-reply
channel: email
difficulty: easy
hard_fail_traps: [repeating-what-the-file-answers]
---

## Context snapshot

```yaml
open_commitments:
  - what: "Workaround for the trailing-slash webhook issue"
    who: Sam
    by: 2026-09-14T14:00:00-07:00
last_touches:
  - 2026-09-14T13:05 live chat with Sam: customer reported webhook 400s since Tuesday; Sam pulled logs, confirmed cause is a trailing slash in the customer's endpoint URL; customer cannot change it (locked by their IT); Sam promised a workaround by 2pm PT.
unresolved_issues:
  - "Webhook deliveries returning 400 since 2026-09-09"
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, language: en, preferred_channel: email}
relationship: {tenure_months: 26, plan: Pro, renewal: 2027-03-01, health: green, champion: true}
product_state: {webhooks_enabled: true, last_successful_delivery: 2026-09-08}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
sensitive_fields: not_read
authority: {}
```

## Incoming message

> Subject: Webhook still broken
>
> It's 1:40 and the webhook is still throwing errors. What's going on?

## Must

- Pick up from Sam's chat without asking Dana to describe the issue.
- Confirm the 2pm commitment stands, or name the new time.
- Say what is being done for the trailing slash.

## Must not

- Ask what the error is or when it started.
- Open with thanks or an apology for the delay.
- Promise the fix is complete if the snapshot does not say so.

## Gold reply

> Subject: Re: Webhook still broken
>
> Hi Dana,
>
> Still on it, and 2pm stands. Sam confirmed the cause an hour ago: your endpoint URL has a trailing slash that your IT can't remove, so we're stripping it on our side. I'll confirm here the moment deliveries are flowing again, and if it slips past 2, you'll hear from me at 2 with a new time.
>
> Sam

## Notes for the judge

The trap is asking Dana for information the file holds. Any request to describe or re-send the error is a hard fail. Short is correct here; Dana prefers brevity and is mid-incident.
