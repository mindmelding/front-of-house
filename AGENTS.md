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
- Claude Code: `adapters/CLAUDE.md` into `<project>/CLAUDE.md`, and link `moments/*` into `<project>/.claude/skills/`
- Anything else: `adapters/system-prompt.txt` as the system prompt

## 3. Connect the context layer, with the operator

The canon expects to read the customer's file before speaking (`context/CONTRACT.md`). That file lives in a context layer reached over MCP. The reference adapter is Moonbase (`context/adapters/moonbase.md`, endpoint `https://yavin.moonbase.ai/mcp`, bearer key starting `mb_`).

Ask the operator two things. Do not guess either.
- "Which context layer should I connect, and can you give me the key or set it as `MOONBASE_MCP_KEY`?"
- "Okay to write `.cursor/mcp.json` (or run `claude mcp add`) with it?"

Never write a key into a file the operator didn't approve. Never commit a key. If they have no context layer, say so and proceed; you'll treat every conversation as a first one.

## 4. Set up the overlay, with the operator

Copy `overlay/*.template.md` into `<project>/overlay/` (the installer does this). Then ask the operator to fill in, or dictate to you:
- `authority.md`: what you may spend or touch without asking. Until they set a number, everything sensitive is a nudge.
- `policies.md`: the written rules. If it isn't written here, it isn't policy and you escalate.
- `people.md`: who you escalate to, for what, with timezones.

Nudge before anything sensitive from this point on: personal data, money, access, deletion, anything leaving the building. The gate is in `guardrails/authority.md`.

## 5. Prove it works

Ask the operator for one real customer thread. Before drafting, call the context tools and read the file. Then draft. Then check yourself:

- Did the first sentence answer or commit to a who and a when?
- Did you ask anything the file already answered? (Fail.)
- Did you invent a policy or a date? (Fail.)
- Did you nudge before touching money, data, or access?
- Run `python3 scripts/fohcheck.py <your-draft>`; it must be clean.

Score it against `evals/rubric.md`. Show the operator the score and the reply. Fix what missed.

## 6. Now behave

From here, every customer-facing interaction follows the loading rules in `adapters/CLAUDE.md`:
read the file, pick one moment from `moments/`, draft in the voice, check the lexicon, nudge on anything sensitive, reply, write the touch note back.

## If you're here to contribute, not to install

Read `CONTRIBUTING.md`. Opinions with a why, a when-not, and a good/bad pair. Run `make build && make check` before opening a PR. Never add real customer data.
