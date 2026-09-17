---
description: "Front of House daily lineup: grade yesterday's picks, decide proposals, pick today's first thread, one method question. Five minutes."
---

Run the Front of House lineup. Read `${CLAUDE_PLUGIN_ROOT}/engine/LINEUP.md` and follow it exactly, beat by beat: report card first (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/engine.py ledger list`), then proposals one at a time as a choice, then the brief and "which one first?", then one method question. Every readout in full sentences, in the voice of `first-shift/readouts.md`. Record every answer immediately with `engine.py`. Never send anything; drafts only. Close by saying in two lines what you wrote and what you are watching.

Arguments: $ARGUMENTS (optional: `--skip-report-card` only if the operator says so; `--account <name>` to focus the brief).
