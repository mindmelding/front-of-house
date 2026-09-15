---
id: first-shift-first-brief
type: process
status: active
last_reviewed: 2026-09-15
---

# The first brief: come back with work

Onboarding that ends with "I'm ready" wasted the operator's fifteen minutes. The First Shift ends with a brief: what needs doing in the window they chose, ranked, drafted, and one delight moment researched ahead of time. Every refreshed in-motion read after that produces the same brief. The agent walks up to the pass with plates, not a menu.

## Inputs

- `overlay/in-motion.md` (just written), scoped to the window in `STATE.md`
- `overlay/customers.md` (who counts)
- `overlay/authority.md` (what's granted; everything else is a nudge)
- the source, for the file behind each item
- whatever research tools the host has: web search, the meeting connector, the usage connector, the operator's memory files

## Opportunities, ranked

Pull candidates from every lens, then rank by **cost of silence**: what gets worse fastest if nobody acts today.

| Lens | What to look for in the window | Playbook |
|---|---|---|
| We owe | promises with a date, overdue first; threads where the last message is theirs | `moments/our-mistake`, `moments/silence` |
| First hundred days | new accounts with no first-value event, no kickoff, or a stalled step | `moments/onboarding-first-100-days` |
| Gone quiet | usage or replies dropped; champion stopped writing | `retention/signals.md`, `moments/silence` |
| Still warm | an incident, an angry thread, a credit issued, within the window | `moments/angry-customer`, `moments/our-mistake` |
| Expansion signal | new seats, a second team, a question about limits, a public hire | `retention/save-plays.md` (the inverse move) |
| Small moment worth a human | the third reset, the same question twice, the invoice question that came with a personal line | `moments/small-moment` |
| Feature ask unanswered | a request that got "noted" and nothing since | `moments/feature-request` |

Keep three to five. For each: one line on why now, the account and person, the draft (channel-correct, in the voice, lexicon-checked), and the file it came from. Draft-only. If the right move is a credit, a refund, reading a field outside the grant, or anything that leaves the building, the draft carries a nudge line instead of the action.

## One delight moment

Exactly one. `delight/catalog.md` lists the triggers; `delight/PHILOSOPHY.md` says why one specific line beats a gift basket. Rules for the brief:

- **Research ahead of time.** Before proposing, look: recent launch, funding, a hire, a talk, a milestone in usage, something they said in a meeting and never got back to. Use web search if the host has it. Cite the source in the brief so the operator can trust the detail.
- **Verified, or skipped.** A milestone the data doesn't show, a win you couldn't confirm, a detail from an unrelated company with the same name: skip. Say "worth a look" instead of drafting.
- **Check history.** Contract row 9. If a gesture already went to this person, pick another person or another trigger.
- **Prefer doing over saying.** The highest tier is the thing built because they mentioned it once. Second is the specific line. Swag is last.
- **Cost tier stated.** Free, under-ceiling, or nudge, per the catalog.

## Output

Present it in the chat in the voice of `first-shift/readouts.md` (the "after" version there is the model), and save the same text to `overlay/briefs/YYYY-MM-DD.md` (never in the canon). The shape:

> Here's what I'd do first, in order.
>
> 1. **Acme, Priya.** The root cause on the webhook failures was due on the 12th and nobody wrote. Draft below; it's an our-mistake reply. One thing to know: the fix needs a credit above your ceiling, so I'll ask before that part.
> 2. **Northwind, Dana.** Day twelve and no import yet. The kickoff notes say she wanted a weekly report by the 30th, so the draft offers to set that up for her.
> 3. **Beacon, Marcus.** Third password reset this quarter. The SSO redirect looks like the cause, so the draft does the reset and offers the two-minute fix.
>
> On the delight: Riverline shipped their public API on Tuesday, per their changelog, and Jo mentioned wanting the quiet-accounts digest on the August 28 call. The draft congratulates them and hands over the digest, built. Costs nothing.
>
> Worth a look but not drafted: Harbor may have raised; I couldn't confirm it.
>
> Drafts follow, one per item, with the channel and the moment labelled.
>
> Which one first?

That reply is the proof thread for the First Shift, and the journal entry that starts the local loop.

## What the brief never does

Never sends. Never acts on a nudge item. Never invents a milestone, a number, or a policy to make an item look better. Never pads to five when there are two. Never buries the overdue promise under the delight. Never reads like a status board; if it can't be said aloud to a colleague, rewrite it.
