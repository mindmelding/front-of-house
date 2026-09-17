---
id: engine-sweep
type: process
status: active
confidence: medium
last_reviewed: 2026-09-17
---

# Sweep

Runs unattended every weekday morning. Reads the delta since the watermark, learns from what the operator sent, proposes at most three changes, ranks what needs doing, holds drafts, and writes a heartbeat. **Asks nothing. Sends nothing. Silent when quiet.**

Invoked by `scripts/sweep.sh` (which `ops/launchd.template.plist` schedules) as a non-interactive agent run. When you are that agent: follow this file top to bottom, run every `engine.py` call exactly as written, and end with the terminal signal in step 8. If a tool fails, record the gap and continue; never substitute a guess for a read.

## 0. Load

`MINDSET.md`, `PRECEDENCE.md`, `guardrails/authority.md`, the overlay (`who.md`, `customers.md`, `authority.md`, `in-motion.md`, `directives.md` if present), `overlay/house/README.md`, and `context/adapters/<source>.md` for the confirmed source. Read `overlay/method.md` if present: it changes what counts as a dropped ball.

```
python3 scripts/engine.py heartbeat start
python3 scripts/engine.py watermark get
```

## 1. Delta

Through the confirmed source, pull everything since the watermark. If the connector's tools did not mount in this session, do not stop: `python3 scripts/mcp_call.py tools` speaks to the same server from `overlay/mcp.json` with the same key, read-only (`mcp_call.py call <tool> '<json>'`, `mcp_call.py accounts --since <iso>`), and say so in the signal. Pull everything since the watermark: messages in and out, meetings, usage changes, for accounts that pass `overlay/customers.md`. Where the adapter warns that one call misses what another sees (the Moonbase adapter does), cross-check before asserting "no record."

Register every account and person you touch before writing anything derived from them:

```
python3 scripts/engine.py alias add "<Account>" --kind account
python3 scripts/engine.py alias add "<Full Name>" --kind person --org "<Account>"
```

## 2. Draft-versus-sent

```
python3 scripts/engine.py drafts list
```

For each held draft, find the message the operator actually sent on that thread since the draft was held.

- Sent and identical, or near enough that only a greeting changed: `drafts resolve <path> --outcome sent-as-is`
- Sent with changes: write the sent text to a temp file, then `drafts resolve <path> --outcome edited --sent-file <tmp> --lesson "<one line, in your words, on what the change says about the house>"`
- Not sent and the thread moved on without it: `drafts resolve <path> --outcome not-sent --lesson "<why, if visible>"`
- Not sent, thread still open: leave it held.

The resolve command journals the outcome and the diff, anonymized. The lesson is yours to write; the diff is the evidence.

## 3. Classify and compare

For every customer-facing message the operator sent in the delta (held draft or not):

1. Name the moment (one of `moments/`). If none fits, it is a new situation (step 4).
2. Read the canon playbook plus `overlay/house/<moment>.md`. Ask: what would the canon plus the house have drafted here, and where does the operator's message differ *in a way that is not already a house rule or a counter-example*?
3. A difference with a shape (not a one-off phrasing) is a candidate. Note it with the account alias and date.

## 4. Propose

A candidate becomes a proposal only at evidence 2: the same shape, twice, across the delta plus the last thirty days of journal and queue. Evidence 1 goes to the queue as well but the queue holds it pending until a second sighting reinforces it (the `queue add` command does this merge itself).

```
python3 scripts/engine.py queue add --moment <m> --kind rule --text "<the rule, one sentence, in the house's voice>" --evidence <n> --source "<Account alias> <date>; <Account alias> <date>"
```

Other kinds: `--kind lexicon` for a customer phrase worth adopting, `--kind method` for something about how the operator works (roles, not names), `--kind new-situation` for a message no moment covers. The command refuses anything denied before. **Cap: three new proposals a day.** Beyond that, hold for tomorrow.

## 5. Brief

Rank what needs doing by cost of silence, per `first-shift/first-brief.md`: we owe, first hundred days, gone quiet, still warm, expansion signal, small moment worth a human, feature ask unanswered. Apply `overlay/directives.md` thresholds and `overlay/method.md` (an ask under a day old is not a stall if the method says same-day is the norm). Three picks maximum; the rest go under a `Held back` heading so nothing is silently dropped.

For each pick, hold a draft:

```
python3 scripts/engine.py drafts hold --account "<Account>" --person "<Name>" --channel <email|slack|chat> --moment <m> --thread "<thread reference>" --file <draft.md>
```

Drafts are in the voice, lexicon-checked (`scripts/fohcheck.py`), with a nudge line instead of any sensitive action. Then write two files:

- `overlay/briefs/YYYY-MM-DD.md`: the brief in the readout voice (`first-shift/readouts.md`), real names, picks numbered, held-back list, one delight moment if one is verified, a `Method watch` line if any of the method's counters tripped (hands-on builds at three, a self-deferred thread past its date, no no-agenda touch in sixty days).
- `overlay/briefs/YYYY-MM-DD.json`: `{"surfaced": [{"rank": 1, "account": "<name>", "headline": "<one line>", "recommended_move": "<one line>", "why_now": "<one line>", "moment": "<moment>"}]}`

```
python3 scripts/engine.py ledger append overlay/briefs/YYYY-MM-DD.json
```

If nothing needs doing, write no brief and say so in the signal.

## 6. Account state (optional, when the source is per-account)

For each account with activity, rewrite `overlay/accounts/<slug>/state.md` per `engine/account-state.md`: verdict on top, prior verdicts stacked, FACT / INFERENCE / ALTERNATIVE labelled, whose court each ball is in, data gaps named. "Nothing changed" is a valid verdict.

## 7. Refresh the in-motion read when stale

If `shift.py status` says the in-motion read is older than seven days, regenerate `overlay/in-motion.md` per `first-shift/in-motion.md` and run `shift.py in-motion --touch`.

## 8. Close

```
python3 scripts/engine.py watermark set <ISO datetime of the newest event read>
python3 scripts/engine.py alias audit
python3 scripts/engine.py heartbeat end --signal "<quiet | N proposals, M picks, K new situations, J drafts resolved>"
```

Then print exactly one line: `SWEEP DONE: <the same signal>`. If any step failed in a way that means the delta was not fully read, print `SWEEP PARTIAL: <what was skipped>` instead and do not move the watermark past what was read.

## What the sweep never does

Never writes outside the overlay and its scratch directory; the canon is tracked and the sweep does not commit. Never asks a question. Never sends. Never moves money, changes access, or shares anything outside the building. Never writes a real name into house, journal, queue, drills, or evals. Never proposes on one occurrence. Never re-proposes a denial. Never fabricates a milestone to make a delight moment work.
