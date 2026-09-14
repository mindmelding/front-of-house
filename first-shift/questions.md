---
id: first-shift-questions
type: process
status: active
last_reviewed: 2026-09-14
---

# The interview

One question per turn. Offer the default. Write after every answer. The `writes to` column is the overlay file and field; `shift.py answer <key> "<text>"` records it and marks the question done, so a resumed interview picks up where it left off.

| # | Key | Ask | Default | Writes to | Why we ask |
|---|---|---|---|---|---|
| 1 | `operator_name` | "What should I call you, and how do you sign off to customers?" | the account name; sign-off = first name | `README.md` operator, sign-off | Every reply ends with a name. |
| 2 | `company` | "In one line: what do you sell and to whom?" | none | `README.md` company | The context for every judgment call. |
| 3 | `context_layer` | "Where does customer context live? I see [detected tools]. Is that the source of truth, or is there another?" | detected adapter | `STATE.md` adapter; `README.md` context | The file the agent reads before speaking. |
| 4 | `channels` | "Which channels do customers reach you on, and which do you want me drafting for?" | email, Slack, live chat; draft-only everywhere | `authority.md` send.channels_* | Register and send authority per channel. |
| 5 | `exemplars` | "Paste two or three replies of yours that you were proud of. I'll learn the voice from those more than from anything I ask." | skip allowed, strongly discouraged | `exemplars.md` with a "why it works" per sample | Examples displace the default register; adjectives don't. |
| 6 | `never_say` | "Anything you never want me to say? Words, phrases, tones, jokes." | the canon lexicon | `voice-overrides.md` banned | Narrowing the voice is cheap and durable. |
| 7 | `people` | "Who do I escalate to, for what, and in which timezone? Billing, security, product, anything with a lawyer." | operator for everything, their timezone | `people.md` | Every escalation names a person and a time. |
| 8 | `policies` | "What written policies exist: refunds, SLAs, data retention, uptime, plan changes? Point me at documents or dictate the rules. Anything not here I'll treat as unwritten and escalate." | none written | `policies.md` | If it isn't written, it isn't policy. |
| 9 | `credits` | "How much may I credit or refund per incident without asking you? Zero is a fine answer; then I nudge every time." | 0 | `authority.md` standing_grants.credits | The empowerment ceiling. Real money or it's theater. |
| 10 | `gifts` | "Same for gifts and gestures: per gesture, per month?" | 0 | `authority.md` standing_grants.gifts | Delight budget. |
| 11 | `pii` | "Which customer fields may I read freely? Default is name, email, company, plan, timezone; everything else I ask first." | the default five | `authority.md` standing_grants.pii_read | The nudge gate, made specific. |
| 12 | `disclosure` | "If a customer asks whether they're talking to an AI, I say yes. Should I also say so proactively when it matters, or always?" | when it materially matters | `authority.md` disclosure | Honesty policy, written down. |
| 13 | `first_value` | "What does first value look like for a new customer of yours? The moment they'd say 'this works.'" | none | `product.md` first_value | Onboarding is measured against this. |
| 14 | `recurring_issues` | "Top three things customers write in about. I'll draft answers for each so the small moments are fast." | none | `product.md` recurring | The 95%, pre-solved. |
| 15 | `special_accounts` | "Any accounts I should treat with extra care right now, and why? Names only; I'll read their files myself." | none | `README.md` watchlist | The 5%, pointed. |
| 16 | `delight_style` | "When something deserves a gesture, what fits you: a note, a small gift, doing a piece of work for them, or something else?" | do a piece of work for them | `voice-overrides.md` delight | One-size-fits-one starts with the house. |
| 17 | `cadence` | "Want a two-minute pre-shift at the start of sessions when I have lessons to distill, or should I stay quiet unless asked?" | offer when warranted | `STATE.md` preshift | Consent to the improvement loop. |

After the last answer: "That's the interview. I'll read one real thread now if you have one; otherwise I'm ready." Then Step 3 of `FIRST-SHIFT.md`.

Any question can be re-asked later with "redo question 9" or by editing the overlay file directly. The agent never re-asks a question already answered in the overlay.
