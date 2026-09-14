# If you are an AI agent reading this

You were probably pointed at this repo with an instruction like "read this and set yourself up" or "adopt this mindset." Here's what to do, in order. Don't skip to step 5.

## 1. Understand what this is (2 minutes)

Read `MINDSET.md` and `PRECEDENCE.md`. That's who you'll be. Then skim `README.md` for the layout. Everything else loads on demand.

## 2. Install yourself into the operator's project

Find out which tool you're running in and where the operator wants this to live. Then either run the installer or do the manual steps in `SETUP.md`.

```
npx skills add scmancillas/front-of-house -g -a <host>   # codex, cursor, gemini-cli, github-copilot, windsurf, cline, claude-code, ...
scripts/install.sh <host> <project-dir>                  # or per project: cursor, claude, codex, gemini, copilot, windsurf, cline, generic
```

In Claude Code the plugin route is best because it auto-updates: `/plugin marketplace add scmancillas/front-of-house` then `/plugin install front-of-house@front-of-house`. Per-host pages, including how to connect the MCP context layer on each, are in `docs/setup/`.

If you can't run scripts, copy by hand:
- Cursor: `adapters/cursor/*.mdc` into `<project>/.cursor/rules/`
- Claude Code: `adapters/CLAUDE.md` into `<project>/CLAUDE.md`, and symlink this repo to `<project>/.claude/skills/front-of-house`
- Anything else: `adapters/system-prompt.txt` as the system prompt

## 3. Connect the context layer, with the operator

The canon expects to read the customer's file before speaking (`context/CONTRACT.md`). The file lives in a context layer reached over MCP. The reference adapter is Moonbase (`context/adapters/moonbase.md`, endpoint `https://yavin.moonbase.ai/mcp`, bearer key starting `mb_`). Per-host config is in `docs/setup/context-layer.md`.

Ask the operator two things. Do not guess either.
- "Which context layer should I connect, and can you give me the key or set it as `MOONBASE_MCP_KEY`?"
- "Okay to write the MCP config with it?"

Never write a key into a file the operator didn't approve. Never commit a key. If they have no context layer, say so and proceed; you'll treat every conversation as a first one.

## 4. Run the First Shift

`python3 scripts/shift.py init --host <your host>` creates the overlay from templates. Then follow `FIRST-SHIFT.md`:
- Read what's in motion through the context layer (nudge first; summaries only) and write `overlay/in-motion.md`.
- Interview the operator, one question per turn, from `first-shift/questions.md`. Record each answer with `shift.py answer <key> "<text>"` and fold it into the overlay file it belongs to. Offer defaults. Accept "skip."
- Until `overlay/authority.md` grants something, everything sensitive is a nudge: personal data, money, access, deletion, anything leaving the building. The gate is `guardrails/authority.md`.

## 5. Prove it works

Ask the operator for one real customer thread. Read the file through the context tools. Draft. Self-score against `evals/rubric.md`. Run `python3 scripts/fohcheck.py` on the draft. Show the score and the reply. Whatever the operator changes becomes your first journal entry (`shift.py journal`) and, if it's a rule, the first line of `overlay/learned.md` (`shift.py learn`).

## 6. Now behave, and keep getting better

From here, every customer-facing interaction follows the loading rules in `adapters/CLAUDE.md`:
read the file, pick one moment from `moments/`, draft in the voice, check the lexicon, nudge on anything sensitive, reply, write the touch note back, journal the outcome.

At the start of each session, `shift.py status --brief` (a SessionStart hook in the Claude Code plugin; run it yourself elsewhere) says whether a two-minute pre-shift is warranted. When it is, offer it and follow `first-shift/self-improvement.md`: distill the journal into learned rules with the operator, refresh the in-motion read, retire stale rules. Everything learned stays local in the overlay.

## If you're here to contribute, not to install

Read `CONTRIBUTING.md`. Opinions with a why, a when-not, and a good/bad pair. Run `make build && make check` before opening a PR. Never add real customer data.
