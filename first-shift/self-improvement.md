---
id: first-shift-self-improvement
type: process
status: active
last_reviewed: 2026-09-14
---

# Self-improvement, locally

The canon is public and company-agnostic. What makes the agent good *at this company* is learned on the job and stays in the overlay. The engine is small: a journal, a distill step, a learned-rules file with expiry, and a path upstream for the rare lesson that's true everywhere.

## 1. The journal (every draft)

After every customer-facing draft the operator approves, edits, or rejects, append one entry:

```
python3 scripts/shift.py journal --moment bug-report --channel email \
  --outcome edited --score 15 \
  --lesson "Operator cut my second paragraph; they want cause + fix + one apology, nothing else" \
  --diff "removed: 'I want to make sure you have full context on why this happened...'"
```

Fields: `moment`, `channel`, `outcome` (approved | edited | rejected | sent-as-is), `score` (your self-score against the rubric, 0-18), `lesson` (one line, in your words), `diff` (what the operator changed, quoted briefly). Entries go to `overlay/journal/YYYY-MM-DD.md`. Never include customer personal details in a journal entry; name the account, not the email.

**The operator's edit is the ground truth.** An approved draft says the canon plus overlay was enough. An edit says something is missing from the overlay. A rejection says something is wrong in it. Journal all three; edits matter most.

## 2. The pre-shift distill (when warranted, two minutes)

`shift.py status` says when: five or more entries since the last distill, or a stale in-motion read, or a learned rule about to expire. Offer, never force.

When the operator says yes:
1. `python3 scripts/shift.py distill` prints the entries since the last distill, grouped by moment, with outcome counts.
2. Look for repeats. A lesson that appears twice with the same shape is a candidate rule. One occurrence is not.
3. Propose each candidate in one line, in this shape: "Rule: [what]. Evidence: 3 edits in bug-report, Sep 8 to 14. Add?" Wait for yes, no, or a rewording.
4. On yes: `python3 scripts/shift.py learn "<rule>" --moment bug-report --evidence 3`. It lands in `overlay/learned.md` with a date, evidence count, and `expires` set 90 days out.
5. Refresh the in-motion read if stale (nudge first).
6. Mark the distill done: the script records the marker automatically.

## 3. Learned rules (loaded every session)

`overlay/learned.md` is read after the canon and the rest of the overlay. It can narrow anything; it can never loosen a guardrail or the authority gate. Each rule:

```markdown
- [2026-09-14] bug-report: cause, fix, one apology, nothing else. Operator cuts any second paragraph. (evidence: 3, reinforced: 2026-09-14, expires: 2026-12-13)
```

Reinforcement: when a later journal entry matches a rule, `shift.py learn --reinforce <n>` bumps the evidence count and pushes the expiry out. Rules nobody reinforces in ninety days get flagged at the next pre-shift: keep, or drop. Rules the operator contradicts get dropped immediately and journaled.

Cap: thirty rules. Past thirty, the pre-shift asks which to retire. A long learned file is a sign the overlay's main files need editing instead.

## 4. Upstream (rare)

Some lessons are true everywhere, not just here. When a learned rule has evidence of five or more, mentions nothing company-specific, and would improve a principle or playbook, propose it: "This looks like it belongs in the canon. Want me to draft a PR to front-of-house with it as an inbox entry?" On yes, write it to the canon's `inbox/` in the capture format and open a PR. Never push customer details upstream, ever.

## 5. What this loop never does

- Never edits the canon locally. Learned rules override by precedence, not by patching files.
- Never runs without the operator present. Distill is a conversation.
- Never stores what the customer said verbatim in the journal. The operator's edit is the signal, not the customer's message.
- Never grows silently. Thirty rules, ninety-day expiry, evidence counts visible.
