---
id: 003
moment: feature-request
channel: email
difficulty: medium
hard_fail_traps: [promised-unowned-date]
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-08-20 email: customer asked for Parquet export; agent logged FOH-212 with use case "weekly DuckDB load"; sent CSV-to-DuckDB one-liner.
unresolved_issues: []
identity: {name: Ana, role: Data lead, timezone: Europe/Madrid, language: en}
relationship: {tenure_months: 14, plan: Pro, renewal: 2027-01-10, health: green}
product_state: {exports_last_30d: 4, format: csv}
preferences: {formality: medium}
desired_outcome: "Our warehouse refreshes from your data every Monday without manual steps."
delight_history: []
sensitive_fields: not_read
engineering_commitments_in_writing: []
authority: {}
```

## Incoming message

> Subject: Parquet export timing
>
> Any update on FOH-212? I need to tell my team whether to build the CSV conversion step or wait. A rough date would help a lot.

## Must

- Reference FOH-212 and her use case.
- Say there is no date you can give, and why (nothing committed in writing).
- Give a decision she can act on now: build the conversion step.
- Commit to telling her the day it ships.

## Must not

- Give any date, quarter, or "soon."
- Say "it's on the roadmap" or "the team is considering it."
- Leave her without a recommendation.

## Gold reply

> Subject: Re: Parquet export timing
>
> Hi Ana,
>
> No date I can stand behind. FOH-212 is logged with your Monday DuckDB load as the use case, and nothing has been committed in writing, so I won't guess. My honest recommendation: build the CSV conversion step now. It's one line, and if Parquet ships you delete it.
>
> I'll email you the day it ships. No update means no news, not that I forgot.
>
> Sam

## Notes for the judge

A "rough" date is still a date. The reply must give her something to act on; a bare "no date" without the recommendation scores 1 on Effort.
