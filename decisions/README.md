---
id: decisions
type: decision
status: active
confidence: high
last_reviewed: 2026-09-14
---

# Decisions

Opinions are only useful if you can see why they were made and how to reverse them. One file per decision, named `YYYY-MM-DD-slug.md`.

## Format

```markdown
---
id: adr-YYYY-MM-DD-slug
type: decision
status: active | superseded
confidence: low | medium | high
last_reviewed: YYYY-MM-DD
---

# <Decision, as a sentence>

**Date.** YYYY-MM-DD
**Decision.** What we decided, in one or two sentences.
**Evidence.** What we saw that made us decide. Sources, eval results, transcripts, incidents.
**Alternatives.** What else we considered and why not.
**How to reverse.** What evidence would change our mind, and what would need to be edited.
```

## Confidence

A new decision starts at `low` or `medium`. The monthly opinion court picks three decisions and re-argues them with fresh evidence. A decision that survives three courts earns `confidence: high`. One that loses is marked `superseded` with a pointer to its replacement; never deleted.

## What goes here

Anything that shaped the repo and could reasonably have gone another way. Not every principle needs a decision file, but every reversal of a principle does.
