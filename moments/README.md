---
id: moments
type: index
status: active
last_reviewed: 2026-09-14
---

# Moments

The customer lifecycle as a taxonomy of moments. Each moment has one playbook in Agent Skills format (`<slug>/SKILL.md`). A playbook tells you what the best person on the floor does in that moment, what an ordinary company does, the steps, the guardrails, and the 5% move.

## How to pick a playbook

1. `MINDSET.md` is always loaded. So is `PRECEDENCE.md`.
2. Read the file (`context/CONTRACT.md` rows 1 and 2) before you pick anything. The moment is often in the file, not in the message.
3. Load the one moment that matches. If the thread spans two (a bug report from someone who is also quiet for 30 days), load the second. Never load more than two.
4. If nothing matches, it's `small-moment`. Most things are.

## The taxonomy

| Moment | Trigger | Playbook | Leans on |
|---|---|---|---|
| First reply | First message from a person we've never spoken to | `first-reply/` | p01, p02, p16 |
| Onboarding, first 100 days | New account or new user; desired outcome not yet reached | `onboarding-first-100-days/` | p21, p03, p10 |
| Bug report | Something is broken and they told us | `bug-report/` | p02, p03, p13, p19 |
| Feature request | They asked for something the product doesn't do | `feature-request/` | p14, p13, p15 |
| Our mistake | Outage, incident, data issue, a promise we missed | `our-mistake/` | p19, p04, p24, p18 |
| Angry customer | Heat in the message, or a thread that has gone bad | `angry-customer/` | p09, p26, p04 |
| Silence | Usage dropped or stopped; a formerly responsive person went quiet | `silence/` | p20, p08 |
| Refund or credit | Money is on the table, asked for or owed | `refund-or-credit/` | p18, p24, p05 |
| Cancellation and offboarding | They want out | `cancellation-and-offboarding/` | p22, p05 |
| Handoff to human | The moment exceeds your authority or your knowledge | `handoff-to-human/` | p25, p26, p23 |
| Small moment | Transactional: reset, invoice line, where-is-setting | `small-moment/` | p28, p07, p17 |
| Their bad day | Layoffs, champion left, exec departure, personal news they raised | `their-bad-day/` | p09, p08, privacy |

## Not yet written

Outage (public comms), security incident, price change, renewal, expansion signal, executive complaint, advocacy ask, milestone, win-back, VIP. Each of these is an inbox item until someone writes it. Until then, use the nearest moment above and `PRECEDENCE.md`.
