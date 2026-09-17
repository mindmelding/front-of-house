# Changelog

Dated lessons. Every promotion from the inbox lands here. This is also the public "what we learned about hospitality this week" feed.

## 2026-09-17

- The engine. The canon now compounds: `engine/README.md` and four verbs. **Sweep** (scheduled, unattended, silent when quiet) reads the delta, diffs every held draft against what the operator actually sent, proposes at evidence two, ranks the day, holds drafts, writes a heartbeat. **Lineup** (`/lineup`, five minutes) grades yesterday's picks first, decides proposals one at a time, picks the first thread, asks one method question. **Drill** (`/drill`) runs three scenarios from the lowest-confidence silos; the operator's answer becomes a house rule and a private eval case. **Refresh** (monthly) expires, consolidates, checks contradictions, prints the two numbers, sends what is true everywhere upstream.
- The house: `overlay/house/<moment>.md`, one per moment, inheriting the canon, diverging only with evidence, a confirmation date, and a ninety-day expiry. Denials are recorded as counter-examples. Confidence per moment is computed. `overlay/learned.md` becomes an index.
- Anonymized at write time. Learning files hold aliases only (`engine.py alias`); operational files keep real names and never leave the overlay. `engine.py alias audit` is the gate before anything goes upstream. A house can now be published or compared without a customer going with it.
- Three moments added: `renewal-and-expansion`, `escalation-and-incident`, `migration-and-export`, each with an eval case.
- `drills/bank/`: fifteen public scenarios, no answers.
- Durability: `engine/DURABILITY.md`, `ops/launchd.template.plist`, `scripts/sweep.sh`, a heartbeat the SessionStart hook reads. Learned from twenty-two in-session routines that died silently in May.
- Merged in from the private cx-kit: the graded-picks ledger, the "report card first" ritual, the method file (how the operator works, roles not names), stacked account state, runbooks written on the second occurrence, the durability rule.
- Lesson: four generations of CX scaffolding existed on one machine and none of them had a loop turning unattended. The design was never the problem; the last wire was. Every verb here has a "done when it ran once on its own" gate.

## 2026-09-15

- The First Shift now looks before it asks. `shift.py discover` inventories the connectors and local docs already on the machine; the agent proposes the customer-context source and confirms it instead of assuming a vendor. Interview questions carry a "look first in" column and arrive as confirmations when the disk already knew. Customer identification is asked once, or proposed as heuristics into `overlay/customers.md`.
- The shift ends with work: a review window chosen from a menu (7, 14, 30 days, custom), then a ranked brief of opportunities and one delight moment researched ahead of time, drafts ready (`first-shift/first-brief.md`). The thread the operator picks is the proof.
- Lesson: an onboarding that ends with "I'm ready" wasted the operator's fifteen minutes. Walk up to the pass with plates.

## 2026-09-14

- Canon created. 28 principles, 12 moment playbooks, voice system with single-source lexicon, context contract with a Moonbase reference adapter, nudge-first authority gate, eval rubric with 20 cases and a mystery-shopper journey, hall of fame and shame, annotated bibliography, generated adapters for Claude Code, Cursor, and system-prompt agents.
- Principle 28 added on day one: don't abstract humans out of the small moments. The transactional interactions are where relationships are built, because they're the frequent ones.
- Decision: the canon is company-agnostic with a private overlay. Opinions that have to survive strangers are sharper.
- Decision: sensitive dimensions (PII, money, access, deletion, external sharing) are nudge-first until an overlay grants them.
