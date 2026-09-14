---
id: adr-2026-09-14-canon-agnostic-with-overlay
type: decision
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# The canon is company-agnostic; company specifics live in an overlay

**Date.** 2026-09-14
**Decision.** Everything in this repo is written for any company with customers. Policies, pricing, refund authority, product names, real transcripts, and named customers live in a separate private overlay that loads after the canon and may override it with an explicit `overrides:` field. Load order: canon, overlay, context graph, conversation.
**Evidence.** Opinions written for strangers are sharper than opinions written for one team; the public handbooks in `sources/BIBLIOGRAPHY.md` got better because they were public. And the failure cases (invented policy, invented pricing) all come from an agent that couldn't tell canon from company fact. Keeping them in different places makes the line visible.
**Alternatives.** A single private repo with everything in it. Faster to start, but the opinions drift into "how we do it here," it can't be shared, and every fork has to strip out the private parts.
**How to reverse.** If the overlay grows larger than the canon, or if every playbook ends up needing an override, the split is wrong. Merge them and go private.
