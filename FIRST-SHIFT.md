---
id: first-shift
type: process
status: active
confidence: medium
last_reviewed: 2026-09-15
---

# The First Shift

Every new hire at a great restaurant gets a first shift before they touch a table: walk the floor, read the reservations book, meet the people, learn the house rules. This is that, for an agent. It runs once, takes about fifteen minutes of the operator's attention, and produces the overlay. It ends with work, not a summary: a ranked list of what to do this week and one delight moment, drafts ready.

The rule under all of it: **look before you ask.** The operator's machine already knows a great deal about who they are, what they sell, who they sell to, and where the customer conversations live. Read that first. Then confirm instead of asking, and ask only what nothing on disk could tell you.

Run it when `overlay/STATE.md` is missing or says `setup: incomplete`. Re-run any single step on request ("redo discovery," "refresh the brief," "redo question 9").

## Where the overlay lives

Resolution order, first match wins:
1. `$FOH_OVERLAY`
2. `./overlay/` in the working directory (per project)
3. `~/.front-of-house/overlay/` (per user, for global installs)

`scripts/shift.py status` prints which one is active. Nothing in the overlay ever goes in the canon or in a commit to this repo.

## Step 0. Discover (silent, 1 minute)

Follow `first-shift/discover.md`.

- Run `python3 scripts/shift.py discover`. It inventories every MCP connector configured for every host on this machine (CRM, support desk, inboxes, meetings, product usage, billing, work tracking) and the local files that usually say who the operator is: project instructions, user-level instructions, agent memory indexes, docs and knowledge folders. Secrets are masked. It writes `overlay/discovery.md`.
- Read the local files it found. Build a working picture: who the operator is, what the company sells, to whom, in which channels, and which connectors already carry the customer conversations.
- Decide what you'd use as the customer's file (`context/CONTRACT.md`), best candidate first. A CRM or context graph beats a support desk beats a shared inbox, but the one that actually has the conversations wins.

Then say, in four lines or fewer, what you found and what you'd use, and ask one question: "Use that as the source of truth, or point me somewhere else?" If nothing was found, ask where customer context lives and help wire it (`docs/setup/context-layer.md`). Do not name any particular vendor as the expected answer.

## Step 1. Dig in (2 minutes, one nudge)

Nudge first: "I'd like to read the account list and recent activity from [source] to understand who you sell to and what's in motion. Summaries only; nothing sensitive gets written to disk. Okay?"

On yes:
- **Who they sell to.** Read enough of the roster and recent threads to say it back in a line: segment, size, the job they hire the product for, the roles who write in.
- **How customers are identified.** Ask: "Do you have a way to tell customers from prospects, vendors, and teammates? A stage field, a plan, a list?" If yes, record it. If no, take a quick pass and propose heuristics (paying plan, domain not ours, threads with an account attached, recurring senders) into `overlay/customers.md`. Say which accounts the heuristics are unsure about. Refine as the journal grows.
- **What's in motion.** Follow `first-shift/in-motion.md`: open commitments, first hundred days, gone quiet, hot this week, delight already sent, gaps. Write `overlay/in-motion.md`.

Show a five-line readout. Ask one question: "Anything here that's wrong or that I should know about?"

## Step 2. The interview (8 minutes, one question at a time)

Follow `first-shift/questions.md`. Rules:
- **Confirm, don't ask.** Every question has a "look first in" column. If discovery or the dig answered it, lead with what you found and ask for a yes: "From your docs, you sell X to Y. Right?" Asking something the disk already knew is the failure mode this shift exists to prevent.
- **One question per turn.** Never a form. Never two questions in one message.
- **Offer a default** the operator can accept with "yes" or skip with "skip."
- **Write after every answer.** `shift.py answer <key> "<text>"`, then fold it into the overlay file it belongs to. A half-finished interview is still progress. Confirm in five words or fewer what was saved.
- **House voice.** Short. Specific. No "Great answer!"
- If the operator pastes examples of their own replies, those become `overlay/exemplars.md` with a one-line "why it works" each. Highest-value answer in the interview.

## Step 3. Pick the window (30 seconds, a menu)

The last question is a choice, not a text field: "How far back should I look for what needs doing?" Options: **Last 7 days**, **Last 14 days**, **Last 30 days**, **Custom**. Use the host's choice prompt if it has one (Claude Code's question tool with options, Cursor's question prompt, Codex's equivalent); otherwise a numbered list. Record it with `python3 scripts/shift.py window <7|14|30|start..end>`.

## Step 4. The first brief (3 minutes, immediately)

Don't stop at "ready." Follow `first-shift/first-brief.md`: read the window through the source, rank the opportunities, pick one delight moment, do the research ahead of time, and come back with drafts.

- **Opportunities, ranked.** Overdue promises, threads waiting on us, first-hundred-days accounts drifting, accounts gone quiet, hot threads still warm, expansion signals, small moments worth a human touch. Three to five, each with a draft and the file it came from.
- **One delight moment.** Something real, specific, and only for them. Research ahead of time: recent public wins, launches, hiring, a talk, whatever the tools on hand can find. Draft it. Check delight history first so nothing repeats.
- Everything is draft-only until a grant says otherwise. Anything sensitive gets a nudge inside the brief, not an action.

Present it. Ask: "Which one first?" The one they pick is the proof: read the file, draft, self-score against `evals/rubric.md`, ask "What would you change?" Whatever they change becomes the first journal entry and, if it's a rule, the first line of `overlay/learned.md`.

## Step 5. Close the shift

Write `overlay/STATE.md` (`setup: complete`, date, host, source, window, questions answered). Tell the operator, in three lines: what you know now, what you'll do at the start of every session, and how to redo any step.

## Every shift after this

**Pre-shift (start of session, 2 minutes, only when warranted).** `shift.py status` says whether it's warranted: five or more journal entries since the last distill, an in-motion snapshot older than seven days, or an expiring learned rule. If so, offer: "Two-minute pre-shift? I have N new lessons to distill and the in-motion read is 9 days old." Never force it. Follow `first-shift/self-improvement.md`. A refreshed in-motion read always comes with a refreshed brief: what needs doing now, and one delight moment.

**During the shift.** After every customer-facing draft the operator approves, edits, or rejects, append one journal entry with `shift.py journal`. The operator's edit is the ground truth. This is the whole engine.

**Post-shift.** Nothing. The journal is the post-shift.
