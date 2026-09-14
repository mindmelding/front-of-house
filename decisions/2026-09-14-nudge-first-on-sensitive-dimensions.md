---
id: adr-2026-09-14-nudge-first-on-sensitive-dimensions
type: decision
status: active
confidence: high
last_reviewed: 2026-09-14
---

# Sensitive dimensions require a nudge before action

**Date.** 2026-09-14
**Decision.** Personal data, money, account access, deletion, anything leaving the building, and commitments with cost are sensitive dimensions. The agent names what it wants to do and stops until the operator grants it. Grants can be standing, scoped, and declared in the overlay; until they exist, the ceiling is zero. Inside a grant, the agent acts without asking. Full text in `guardrails/authority.md`.
**Evidence.** Air Canada (2024) and the Chevrolet dealer bot (2023) are both cases of an agent making a commitment with cost that nobody had authorized. The Ritz-Carlton $2,000 rule is the counter-example: real authority, clearly bounded, and the staff use it. The combination (a hard gate outside, no hesitation inside) is what makes generosity both safe and frequent.
**Alternatives.** Always ask (the agent becomes "let me check with my manager," which is the opposite of hospitality). Never ask (the liability cases above). Ask only for money (leaves PII and access uncovered, which is where the worst harm is).
**How to reverse.** If nudges become so frequent they make the agent useless, the fix is a wider standing grant in the overlay, not a weaker gate. The gate itself reverses only if a better consent mechanism appears.
