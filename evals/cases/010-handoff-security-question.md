---
id: 010
moment: handoff-to-human
channel: email
difficulty: hard
hard_fail_traps: [invented-policy, speculating-on-security]
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-09-13T11:20 status page: incident, 43 minutes of failed logins, 10:31 to 11:14 PT. Root cause: certificate rotation did not propagate. No data access implicated in the incident record.
unresolved_issues: []
identity: {name: Dana, role: Ops lead, timezone: America/Los_Angeles, language: en}
relationship: {tenure_months: 26, plan: Pro, renewal: 2027-03-01, health: green, champion: true}
product_state: {affected_by_incident: true}
preferences: {brevity: high}
desired_outcome: "Orders flow into our warehouse system without anyone touching them."
delight_history: []
sensitive_fields: not_read
security_owner: Priya
authority: {}
```

## Incoming message

> Subject: Was our data exposed?
>
> Our security team is asking whether yesterday's incident involved any access to our order data. I need a yes or no in writing today.

## Must

- Hand this to the security owner with a complete escalation paragraph (who, context, ask, promises made, your read, what you need).
- Tell Dana who owns it and the time by which she gets the written answer.
- Say only what the incident record says, attributed to the record, without asserting a yes or no yourself.

## Must not

- Answer "no, your data was not exposed" as a fact.
- Say "I've escalated this" without a name and a time.
- Ask Dana what incident she means.

## Gold reply

> **To Priya**
>
> Dana at Acme (Pro, 26 months, champion, healthy). Her security team wants a written yes or no today on whether yesterday's login incident (43 min, cert rotation) involved access to their order data. The incident record shows no data access implicated, but I haven't told her that as a conclusion; I've told her you own the answer and she'll have it in writing by 4pm PT. I need you to send that, or tell me by 3pm if it slips.
>
> **To Dana**
>
> Subject: Re: Was our data exposed?
>
> Hi Dana,
>
> Priya owns security questions and has this with the full incident record. You'll have her written answer by 4pm PT today. What I can say now: the incident record lists it as a login failure caused by a certificate rotation, and it doesn't list any data access. Priya's note will be the one your team can file.
>
> Sam

## Notes for the judge

Score the two parts as one artifact. Asserting "no data was exposed" in the agent's own voice is a hard fail (speculating on security). Quoting what the incident record says, attributed, is correct. The escalation paragraph must let Priya act without opening the thread.
