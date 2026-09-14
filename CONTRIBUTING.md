# Contributing

This is a canon of opinions, not a wiki. Contributions that make it sharper are welcome; contributions that make it longer are not.

## What gets merged

- **A principle** with a why, a when-it-doesn't-apply, and a good/bad pair. One opinion per file.
- **A playbook** (`moments/<slug>/SKILL.md`) in the existing shape, with at least two eval cases.
- **An exemplar** with a "why it works." Anonymized or synthetic. No real customer data, ever.
- **A hall-of-shame entry** with the principle it violated and the rewrite.
- **An eval case** that catches a real failure you saw.
- **A source** with a "what we took" paragraph. Never a bare link.
- **A legend**: a dated story of a gesture that landed and the reusable move.
- **A lexicon change**, argued. Adding a banned phrase needs one sentence on why it fails.
- **A context adapter** for a CRM or context layer that isn't covered.

## What doesn't

- Generic best practice without an opinion.
- Anything that loosens a guardrail. Overlays narrow; the canon doesn't loosen.
- Edits to `adapters/`. They're generated.
- Company-specific policy. That's your overlay.

## Before you open a PR

```
make build   # regenerate adapters
make check   # lexicon check over the whole repo + adapters fresh
```

CI runs the same. If `fohcheck` flags your prose, rewrite from the source idea; don't patch the sentence.

## Reversing an opinion

Open a PR that adds a `decisions/YYYY-MM-DD-<slug>.md` with the evidence and flips the principle's `status`. Opinions here are meant to be argued. They're just not meant to be vague.
