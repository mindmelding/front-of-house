---
description: "Front of House sweep, run by hand: read the delta, diff held drafts against what was sent, propose, brief, hold drafts. Non-interactive; the scheduled job runs this same spec."
---

Run the Front of House sweep now, exactly as the scheduled job would. Read `${CLAUDE_PLUGIN_ROOT}/engine/SWEEP.md` and follow it top to bottom without asking any question. Use the overlay's confirmed context source through its adapter. Register every account and person with `engine.py alias add` before writing anything derived from them. End with `engine.py heartbeat end --signal "<signal>"` and one line: `SWEEP DONE: <signal>` or `SWEEP PARTIAL: <what was skipped>`.

Arguments: $ARGUMENTS (optional: `--since <ISO datetime>` overrides the watermark for this run only).
