---
id: adr-2026-09-17-house-by-moment-anonymized-at-write
type: decision
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# What the agent learns is split by moment and anonymized at write time; what it does stays private and real

**Date.** 2026-09-17
**Decision.** Local learning lives in `overlay/house/<moment>.md`, one file per canon moment, inheriting the canon and diverging only with evidence, confirmation, and expiry. Every learning file (house, journal, queue, drills, private evals, lexicon, method) is written through an anonymizer that replaces registered accounts, people, and domains with stable aliases and scrubs emails, phones, and record links. Operational files (in-motion, briefs, held drafts, ledger, directives, account state) keep real names and never leave the overlay.
**Evidence.** A flat `learned.md` with thirty rules reads as a list, not as "how we do refunds"; splitting by moment makes confidence per silo computable and visible, which is what "industry standard, then dial in" needs. Anonymizing at write time, rather than at share time, is the only version that survives contact with a real week: a share-time scrub depends on someone remembering to run it. The operator asked for exactly this: capture how they respond, anonymized. It also makes a house comparable across teams, which is the point of a public scenario bank.
**Alternatives.** One flat rules file (rejected: no per-silo confidence, reads as a list). Anonymize at share time (rejected: relies on memory, and a leak is irreversible). Keep learning and operational files in one tier with real names (rejected: nothing could ever be published or compared). Aliases that are random tokens (rejected: house files become unreadable; stable word aliases keep them legible for months).
**How to reverse.** If the alias audit proves insufficient in practice (a story identifies an account without its name), tighten the writing rule in `engine/ANONYMIZATION.md` first. If per-moment files fragment the house so that cross-cutting rules have no home, add `overlay/house/_all.md` for rules with `moment: all` and revisit. Edit `engine/README.md`, `engine/ANONYMIZATION.md`, `scripts/engine.py`.
