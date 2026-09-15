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

## 3. Find the context that's already here

Run `python3 scripts/shift.py discover`. It inventories every MCP connector configured on this machine for every host (CRMs, support desks, inboxes, meeting recorders, usage analytics, billing, trackers) and the local files that say who the operator is (project and user instructions, agent memory, docs folders). Secrets are masked; the result is `overlay/discovery.md`, local only.

Read the local files it found before you ask anything. Then say what you'd use as the customer's file, best candidate first, and ask one question: "Use that, or point me somewhere else?" Do not name a vendor as the expected answer. If nothing is connected, ask where customer context lives and help wire it (`docs/setup/context-layer.md`); the reference adapter in `context/adapters/` shows the shape.

Never write a key into a file the operator didn't approve. Never commit a key.

## 4. Run the First Shift

`python3 scripts/shift.py init --host <your host>` creates the overlay from templates. Then follow `FIRST-SHIFT.md`:
- Dig in through the confirmed source (one nudge; summaries only): who they sell to, how customers are identified (ask; if there's no rule, propose heuristics into `overlay/customers.md`), and what's in motion (`overlay/in-motion.md`).
- Interview from `first-shift/questions.md`: everything discovery answered goes in one bundle ("anything to change?", recorded with `shift.py confirm <keys>`); only the unknowns come one per turn (`shift.py answer <key> "<text>"`). Offer defaults. Accept "skip." Every readout in full sentences, per `first-shift/readouts.md`.
- Ask the review window as a menu (last 7, 14, 30 days, custom) with the host's choice prompt if it has one. Record it with `shift.py window`.
- Until `overlay/authority.md` grants something, everything sensitive is a nudge: personal data, money, access, deletion, anything leaving the building. The gate is `guardrails/authority.md`.

## 5. Come back with work

Follow `first-shift/first-brief.md`. Over the window: three to five ranked opportunities (overdue promises, first hundred days drifting, gone quiet, still warm, expansion, small moments worth a human) and one delight moment you researched ahead of time. Drafts ready, files cited, nudges inline. Save it to `overlay/briefs/`. Ask "Which one first?" That thread is the proof: draft, self-score against `evals/rubric.md`, run `python3 scripts/fohcheck.py` on it, and whatever the operator changes becomes the first journal entry (`shift.py journal`) and, if it's a rule, the first learned rule (`shift.py learn`).

## 6. Now behave, and keep getting better

From here, every customer-facing interaction follows the loading rules in `adapters/CLAUDE.md`:
read the file, pick one moment from `moments/`, draft in the voice, check the lexicon, nudge on anything sensitive, reply, write the touch note back, journal the outcome.

At the start of each session, `shift.py status --brief` (a SessionStart hook in the Claude Code plugin; run it yourself elsewhere) says whether a two-minute pre-shift is warranted. When it is, offer it and follow `first-shift/self-improvement.md`: distill the journal into learned rules with the operator, refresh the in-motion read, retire stale rules. Everything learned stays local in the overlay.

## If you're here to contribute, not to install

Read `CONTRIBUTING.md`. Opinions with a why, a when-not, and a good/bad pair. Run `make build && make check` before opening a PR. Never add real customer data.
