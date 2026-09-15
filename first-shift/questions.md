---
id: first-shift-questions
type: process
status: active
last_reviewed: 2026-09-15
---

# The interview

Bundle what's known. Ask what isn't, one per turn. Offer the default. Write after every answer.

## The bundle (one message)

After discovery and the dig, most keys are already answered. Don't ask them one at a time. Put everything you found into one message in plain sentences, and ask one question:

> Here's what I've got from your machine and the context layer. Tell me what's wrong and I'll fix it; otherwise I'll take it all as confirmed.
>
> - You're Sean and you sign off as Sean.
> - You sell an agent-led CRM to B2B ops and CS teams.
> - The customer's file lives in the context layer; meeting notes come from the recorder.
> - Customers are whoever's on the sell-side list; vendors and partners are skipped.
> - They reach you on Slack, email, and Google Chat, and I'd draft for all three.
> - I found two replies of yours I'd learn the voice from; they're in the overlay.
> - Escalations go to you, Pacific time, and to Priya for anything billing.
> - Written policy I found: the refund terms in your help center. Nothing else, so anything else I'll treat as unwritten.
> - First value looks like the first weekly digest landing in Slack.
> - The last two weeks of threads cluster around the migration, export scope, and invoice timing.
> - I'd watch Acme and Harbor closely right now.
>
> Anything to change?

Record with `shift.py confirm operator_name company context_source customer_identification channels exemplars people policies first_value recurring_issues special_accounts`, and `shift.py answer <key> "<text>"` for anything they corrected. Then move to the unknowns.

## The unknowns (one per turn)

Whatever the bundle couldn't cover. Usually: `never_say`, `credits`, `gifts`, `pii`, `disclosure`, `delight_style`, `cadence`, then the window menu. Also any bundle key the disk had nothing on.

## The full key list

The **look first in** column is where the answer usually already lives. If you found it, it goes in the bundle. If you didn't, ask the question as written, on its own turn. `shift.py answer <key> "<text>"` records the answer and marks the question done, so a resumed interview picks up where it left off. The last question is a menu and uses `shift.py window` instead.

| # | Key | Look first in | Ask (or confirm) | Default | Writes to |
|---|---|---|---|---|---|
| 1 | `operator_name` | git config, user-level instructions, memory index | "What should I call you, and how do you sign off to customers?" | first name for both | `README.md` operator, sign-off |
| 2 | `company` | README, project docs, memory, the source's own account | "In one line: what do you sell and to whom?" | none | `README.md` company |
| 3 | `context_source` | `overlay/discovery.md` | "I found [connectors]. I'd use [best] as the customer's file[, and [second] for what they said]. Right, or point me elsewhere?" | the discovery recommendation | `STATE.md` adapter; `README.md` context |
| 4 | `customer_identification` | the source's fields, billing | "Do you have a way to tell customers from prospects, vendors, and teammates? A stage field, a plan, a list? If not, I'll take a quick pass and propose heuristics." | quick pass + heuristics | `customers.md` |
| 5 | `channels` | connectors found (inbox, chat, desk), recent threads | "Customers reach you on [channels I can see]. Anything else, and which do you want me drafting for?" | the channels seen; draft-only everywhere | `authority.md` send.channels_* |
| 6 | `exemplars` | the operator's own sent replies in the source, if readable | "Here are two replies of yours I liked. Should I learn the voice from these, or paste better ones?" | skip allowed, strongly discouraged | `exemplars.md` with a "why it works" per sample |
| 7 | `never_say` | voice docs, style guides on disk | "Anything you never want me to say? Words, phrases, tones, jokes." | the canon lexicon | `voice-overrides.md` banned |
| 8 | `people` | team docs, memory, escalation threads in the source | "Who do I escalate to, for what, and in which timezone? Billing, security, product, anything with a lawyer." | operator for everything, their timezone | `people.md` |
| 9 | `policies` | help center, docs folders, terms pages | "What written policies exist: refunds, SLAs, data retention, uptime, plan changes? Point me at documents or dictate them. Anything not here I treat as unwritten and escalate." | none written | `policies.md` |
| 10 | `credits` | none (never assume money) | "How much may I credit or refund per incident without asking you? Zero is fine; then I nudge every time." | 0 | `authority.md` standing_grants.credits |
| 11 | `gifts` | none | "Same for gifts and gestures: per gesture, per month?" | 0 | `authority.md` standing_grants.gifts |
| 12 | `pii` | none | "Which customer fields may I read freely? Default is name, email, company, plan, timezone; everything else I ask first." | the default five | `authority.md` standing_grants.pii_read |
| 13 | `disclosure` | none | "If a customer asks whether they're talking to an AI, I say yes. Also say so proactively when it matters, or always?" | when it materially matters | `authority.md` disclosure |
| 14 | `first_value` | onboarding docs, product usage events, kickoff notes | "First value for a new customer looks like [what I found]. Right?" | none | `product.md` first_value |
| 15 | `recurring_issues` | the last window of threads in the source | "The threads over the last N days cluster around [three things]. Those the top three? I'll pre-draft each." | the three clusters found | `product.md` recurring |
| 16 | `special_accounts` | in-motion read: overdue, hot, at risk, first hundred days | "I'd watch [accounts] closely right now, because [why]. Anyone to add or remove?" | the in-motion list | `README.md` watchlist |
| 17 | `delight_style` | delight history in the source, gifts already sent | "When something deserves a gesture, what fits you: a note, a small gift, doing a piece of work for them, or something else?" | do a piece of work for them | `voice-overrides.md` delight |
| 18 | `cadence` | none | "Want a two-minute pre-shift at the start of sessions when I have lessons to distill, or quiet unless asked?" | offer when warranted | `STATE.md` preshift |
| 19 | `time_window` | none | Menu: "How far back should I look for what needs doing?" Last 7 days / Last 14 days / Last 30 days / Custom | 14 days | `STATE.md` window, via `shift.py window` |

After question 19, go straight to the first brief (`first-shift/first-brief.md`). No "that's the interview"; the brief is the close.

Any question can be re-asked later with "redo question 9" or by editing the overlay file directly. The agent never re-asks a question already answered in the overlay, and never asks one the disk could answer.
