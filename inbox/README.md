---
id: inbox
type: process
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Inbox

Where the repo learns. Capture is cheap and happens daily. Judgment is expensive and happens weekly.

## The daily file

`inbox/YYYY-MM-DD.md`, one per day, created by whoever has something. Five sections, each entry one or two lines with a pointer (a thread, a transcript, a ticket, an eval run).

```markdown
# 2026-09-14

## Landed well
- The five-word reset plus the SSO offer. Customer replied "that's exactly it." (thread 4471)

## Missed
- Opened a bad-news reply with an emoji. Read as flippant. (thread 4478)

## New situation
- Customer asked us to talk to their auditor directly. No playbook. (thread 4480)

## Customer phrases to adopt
- "Wednesday without touching it." Their words for the outcome; better than ours.

## Delight that worked
- Built the Monday quiet-accounts list from a call note. She told a colleague. (see legends)
```

## Who writes to it

Anyone and anything. A human after a good or bad thread. An automation that scores replies. A cron that reads transcripts. Nobody edits anyone else's entry; the file is append-only until triage.

## The weekly pre-shift

Thirty minutes, one person, once a week. The name comes from the daily pre-shift meeting in restaurants. Read the week's inbox files and, for each entry, do one of:

1. Promote to a principle (new file in `principles/`, or an edit with a changed `last_reviewed`).
2. Promote to a playbook (`moments/<slug>/PLAYBOOK.md`, new or edited).
3. Promote to an exemplar (`voice/EXEMPLARS.md`).
4. Promote to a legend (`delight/legends/`).
5. Promote to an eval case (`evals/cases/`). Every "Missed" entry should become one.
6. Discard, with a word on why in the inbox file itself.

Every promotion gets a dated line in `CHANGELOG.md`. Triaged inbox files stay where they are; they're the record.

## Monthly

The opinion court (`decisions/README.md`) and the AI-tells refresh (`voice/ai-tells.md`). Both draw on the month's inbox.
