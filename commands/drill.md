---
description: "Front of House drill: three scenarios from the lowest-confidence silos; the operator's answer becomes a house rule and a private eval case. Fifteen minutes."
---

Run a Front of House drill session. Read `${CLAUDE_PLUGIN_ROOT}/engine/DRILL.md` and follow it. Start with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/engine.py drill next --n 3` (or the moment or scenario id in $ARGUMENTS). For each scenario: set the table, ask "you first or me first?", score both against `evals/rubric.md`, name the delta in one sentence, ask "what's the rule?", then record with `engine.py drill record`. Never show a gold reply before the operator has answered. Stop after three or when the operator says stop, and say which silos moved.
