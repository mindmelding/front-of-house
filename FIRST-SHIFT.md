---
id: first-shift
type: process
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# The First Shift

Every new hire at a great restaurant gets a first shift before they touch a table: walk the floor, read the reservations book, meet the people, learn the house rules. This is that, for an agent. It runs once, takes about fifteen minutes of the operator's attention, and produces the overlay. After that, every shift starts with a two-minute pre-shift and ends with a journal entry, and the agent gets better at this company specifically, locally, without touching the canon.

Run it when `overlay/STATE.md` is missing or says `setup: incomplete`. Re-run any single step on request ("redo the interview," "refresh what's in motion").

## Where the overlay lives

Resolution order, first match wins:
1. `$FOH_OVERLAY`
2. `./overlay/` in the working directory (per project)
3. `~/.front-of-house/overlay/` (per user, for global installs)

`scripts/shift.py status` prints which one is active. Nothing in the overlay ever goes in the canon or in a commit to this repo.

## Step 0. Orient (silent, 30 seconds)

- Run `python3 scripts/shift.py status`. It reports: overlay location, setup state, which context adapter is configured, journal entries since the last distill, and whether the in-motion snapshot is stale.
- Detect your host and which context tools are connected (for Moonbase: `ask_account`, `list_events`, `get_event`, `list_accounts`). If none, note it; the interview will ask where the customer context lives.

## Step 1. Read what's in motion (2 minutes, one nudge)

Nudge first: "I'd like to read the account list and recent activity from the context layer to understand what's in motion. Summaries only; nothing sensitive gets written to disk. Okay?"

On yes, follow `first-shift/in-motion.md`: pull the portfolio shape, open commitments, accounts in onboarding, accounts gone quiet, anything hot in the last seven days. Write `overlay/in-motion.md` as a dated summary. Show the operator a five-line readout and ask one question: "Anything here that's wrong or that I should know about?"

## Step 2. The interview (10 minutes, one question at a time)

Follow `first-shift/questions.md`. Rules:
- **One question per turn.** Never a form. Never two questions in one message.
- **Offer a default** the operator can accept with "yes" or skip with "skip."
- **Write after every answer.** Each answer lands in its overlay file immediately, so a half-finished interview is still progress. Confirm in five words or fewer what was saved.
- **Ask in the house voice.** Short. Specific. No "Great answer!"
- Order matters: the questions go from cheap and concrete (your name, your sign-off) to the ones that need thought (authority ceilings). Momentum first.
- If the operator pastes examples of their own replies, those become `overlay/exemplars.md` with a one-line "why it works" each. This is the single highest-value answer in the interview.

## Step 3. Proof (3 minutes)

Ask for one real thread. Read the file through the context layer. Draft. Self-score against `evals/rubric.md`. Show the score and the draft. Ask: "What would you change?" Whatever they change becomes the first journal entry and, if it's a rule, the first line of `overlay/learned.md`.

## Step 4. Close the shift

Write `overlay/STATE.md` (`setup: complete`, date, host, adapter, question count answered). Tell the operator, in three lines: what you know now, what you'll do at the start of every session, and how to redo any step.

## Every shift after this

**Pre-shift (start of session, 2 minutes, only when warranted).** `shift.py status` says whether it's warranted: five or more journal entries since the last distill, or an in-motion snapshot older than seven days, or an expiring learned rule. If so, offer: "Two-minute pre-shift? I have N new lessons to distill and the in-motion read is 9 days old." Never force it. Follow `first-shift/self-improvement.md`.

**During the shift.** After every customer-facing draft the operator approves, edits, or rejects, append one journal entry with `shift.py journal`. The operator's edit is the ground truth. This is the whole engine.

**Post-shift.** Nothing. The journal is the post-shift.
