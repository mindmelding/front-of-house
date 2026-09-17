---
id: engine-lineup
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Lineup

The daily pre-service meeting, in restaurant terms: five minutes, standing up, before the doors open. Runs only when the SessionStart hook says there is something to decide. Four beats, in this order, and the order is the point: **you close the loop on yesterday before you open anything new.**

Everything here is a conversation. Full sentences, in the voice of `first-shift/readouts.md`. Never a status board. One question at a time.

## 0. Load

`python3 scripts/engine.py status` for the counts. Then the newest `overlay/briefs/*.md`, `overlay/queue/PENDING.md`, `overlay/directives.md`, `overlay/method.md`. Skim `overlay/house/README.md` for the confidence column.

## 1. Report card, always first, never skipped

```
python3 scripts/engine.py ledger list
```

For each pending pick, one line: what you surfaced, then the question, plainly: *did you act on it, and was it the right call?* Record the answer immediately:

```
python3 scripts/engine.py ledger grade "<id>" --acted yes|no --verdict right|premature|wrong|noise|superseded --note "..."
```

If the operator names something you held back that turned out to matter: `engine.py ledger miss "<Account>" "<what you missed>"`. Backlog rule: five per session, and say how many remain. Do not move on until the list is empty or the operator says leave it.

**Then codify.** A verdict that changes nothing was wasted. Two premature picks of the same shape, or a miss with a visible cause, become a line in `overlay/directives.md` under "Learned from outcomes," citing the ledger ids. Tell the operator what you wrote.

## 2. Proposals, one at a time

```
python3 scripts/engine.py queue list
```

Present each as a choice, using the host's choice prompt when it has one: **Approve** / **Reword** / **Deny** / **Later**. Show the evidence (the aliased sources) so the operator can trust it. Record the decision:

```
python3 scripts/engine.py queue decide <id> approve
python3 scripts/engine.py queue decide <id> reword --text "<their sentence, verbatim>"
python3 scripts/engine.py queue decide <id> deny --why "<their reason, verbatim>"
python3 scripts/engine.py queue decide <id> later
```

Approve writes the house rule with evidence and expiry. Deny writes the counter-example so it never comes back. The operator's wording always wins over yours.

## 3. The brief

Read out today's picks from the brief, in order, each a sentence or two with the why and the held draft's location. Then the delight moment if there is one, then the held-back list in one line. Ask: **"Which one first?"**

The one they pick: open the held draft, revise with them, run `scripts/fohcheck.py` on it. If they want it as a real draft in their mail or chat client, create it through the connector as a **draft only**, never a send. Say where it is. The sweep will read what they sent tomorrow.

## 4. One method question

Exactly one, from the open questions at the bottom of `overlay/method.md`. Never a batch. Record the answer: mark the entry `[confirmed <date>]` or strike it, and add a rule to `overlay/directives.md` if the answer changes what counts as a dropped ball.

## Close

Say, in two lines, what was written and what you are watching next, and `python3 scripts/engine.py sync status` for the commits this lineup produced (every decision above committed itself). Then stop. A lineup that changed no file was a chat.

## Rules

- Report card before anything new. No exceptions.
- Three interruptions a day, maximum. The rest is held back, visibly.
- Never send. The draft is the human gate.
- Never invent activity. If it is not in the brief, the journal, or the source, say so.
- The operator's edit, verdict, and wording are ground truth. Yours are proposals.
