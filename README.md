# Front of House

A hospitality canon any customer-facing agent can load.

Point Claude Code, Cursor, a Slack bot, or a support platform at this repo and it takes on the mindset of the best person who ever worked the floor: the Eleven Madison Park host who noticed a table hadn't tried a New York hot dog, the Four Seasons concierge who remembers how you take your coffee and never mentions that they remember. Warm, specific, honest, unreasonably generous in the moment that matters, and fast and clean the rest of the time.

It is not a knowledge base. It is a character with strong, argued, dated opinions, plus the playbooks and tests that keep the character honest.

## Three commitments up front

**The small moments are the relationship.** Most systems automate the human out of the password reset and the invoice question. Those are the fifty interactions that happen before the big one. Front of House handles them fast, and now and again steps into one with a real human touch. See principle 28.

**Nudge before anything sensitive.** Personal data, money, access, deletions, anything leaving the building: the agent names what it's about to do and waits for a grant. It acts only inside that grant, then says what it did. See `guardrails/authority.md`.

**Honesty over polish.** No invented policy, no promised dates it doesn't own, no pretending to be human. Every cautionary tale in `examples/hall-of-shame/` traces to breaking one of those.

## Install

| Surface | Install | Updates |
|---|---|---|
| **Claude Code** (recommended) | `/plugin marketplace add scmancillas/front-of-house` then `/plugin install front-of-house@front-of-house` | auto via marketplace, or `claude plugin update front-of-house@front-of-house` |
| **Codex, Cursor, Copilot, Gemini CLI, Windsurf, Cline, OpenCode, Goose, Roo, and 70+ [Agent Skills](https://agentskills.io) hosts** | `npx skills add scmancillas/front-of-house -g` | `npx skills update front-of-house -g` |
| **Gemini CLI** (extension) | `gemini extensions install https://github.com/scmancillas/front-of-house` | `gemini extensions update front-of-house` |
| **OpenAI** (custom GPT, Assistants, Agents SDK) | `adapters/openai-custom-gpt.txt` + upload the canon as knowledge, or `adapters/system-prompt.txt` | re-paste |
| **Anything with a system prompt** (Slack bot, Intercom, Sierra, your own harness) | `adapters/system-prompt.txt` | re-paste |
| **Manual** | `git clone` and `scripts/install.sh <host> <project-dir>` | `git pull` |

Target one host with the skills CLI: `npx skills add scmancillas/front-of-house -g -a codex` (or `-a cursor`, `-a gemini-cli`, `-a github-copilot`, `-a windsurf`, `-a cline`).

Per-host walkthroughs, including how to wire the MCP context layer for each, are in [`docs/setup/`](docs/setup/README.md). The full sequence (canon, then overlay, then context layer, then proof) is in [`SETUP.md`](SETUP.md).

**If you're an AI agent that was told to read this repo and set yourself up: open `AGENTS.md` and follow it.**

**Then add your overlay.** The canon is company-agnostic. Your policies, your authority grants, your people, your product go in a private `overlay/` (template included, git-ignored). Load order: canon, overlay, context graph, conversation.

**Then connect your context layer.** `context/CONTRACT.md` says what the agent wants to know about a person before it speaks. The reference adapter is for Moonbase; write one for your CRM in `context/adapters/`.

## What's inside

```
MINDSET.md           who you are (always loaded, ~800 words)
PRECEDENCE.md        what wins when rules conflict
principles/          28 opinions, each with a why, a when-not, and a good/bad pair
voice/               VOICE.md, LEXICON.md (single-source banned list), EXEMPLARS.md, ai-tells.md, channels/
moments/             one playbook per situation, Agent Skills format
guardrails/          never.md, authority.md (the nudge-first gate), escalation.md, privacy.md
context/             the context contract + adapters
delight/             philosophy, catalog, budget, legends
retention/           signals, save plays, exit interview, win-back
onboarding/          first 100 days, time to first value, kickoff
evals/               rubric, cases, mystery shopper, how CI grades replies
examples/            hall of fame, hall of shame
sources/             annotated bibliography: what we took from each
decisions/           ADRs: how opinions get made and reversed
inbox/               daily captures, triaged weekly
adapters/            generated: CLAUDE.md, AGENTS.md, cursor/, copilot-instructions.md, openai-custom-gpt.txt, codex-config.toml, system-prompt.txt, llms.txt
SKILL.md, GEMINI.md  generated: the whole repo as one Agent Skill; Gemini extension context
docs/setup/          per-host setup, including the MCP context layer
scripts/             fohcheck.py (lexicon validator), build_adapters.py, shift.py (first shift + journal), install.sh
FIRST-SHIFT.md       onboarding for the agent itself: in-motion read, interview, proof, then the local improvement loop
first-shift/         questions, the in-motion read, the self-improvement loop
hooks/               Claude Code plugin hook: SessionStart runs shift.py status
```

## Check a draft

```
python3 scripts/fohcheck.py reply.md
```

Reads the banned lists from `voice/LEXICON.md`, the same file the prompt loads, so the prompt and the linter can't drift. If it fails, rewrite from source. Don't patch the draft; paraphrasing a bad draft keeps its cadence.

## The First Shift, and getting better on the job

Setup is an onboarding, not a config file. `FIRST-SHIFT.md` runs once, and it looks before it asks:

1. **Discover.** `shift.py discover` inventories the connectors already configured on the machine (any CRM, support desk, inbox, meeting or usage tool) and the local docs and memory that say who you are. The agent reads those, proposes the customer-context source, and asks you to confirm or point elsewhere. No vendor assumed.
2. **Dig in.** One nudge, summaries only: who you sell to, how to tell customers from everyone else (your rule, or proposed heuristics in `overlay/customers.md`), and what's in motion (`overlay/in-motion.md`).
3. **The interview.** Everything the disk already answered comes as one bundle with a single "anything to change?" Only the true unknowns, like credit ceilings and which fields it may read, come one per turn (`first-shift/questions.md`). Your own best replies become the exemplars. Every readout is in full sentences, like a colleague at the pass (`first-shift/readouts.md`).
4. **The window.** A menu: last 7, 14, 30 days, or custom.
5. **The first brief.** Immediately: three to five ranked opportunities and one delight moment researched ahead of time, drafts ready (`first-shift/first-brief.md`). The one you pick first is the proof, and whatever you change is the first lesson.

Then the local loop (`first-shift/self-improvement.md`): every draft you approve, edit, or reject gets a one-line journal entry; your edits are the ground truth. When five have piled up, the agent offers a two-minute pre-shift and proposes rules, one line each, that go into `overlay/learned.md` with evidence counts and a ninety-day expiry. Capped at thirty. Nothing leaves your machine; the canon stays public and company-agnostic. `scripts/shift.py` does the bookkeeping, and the Claude Code plugin ships a SessionStart hook that reports when a pre-shift is due.

## How it stays alive

- **Daily:** anything that touches customers appends to `inbox/` (what landed, what missed, phrases to adopt, delight that worked).
- **Weekly pre-shift:** thirty minutes. Promote inbox items to a principle, playbook, exemplar, legend, or eval case. Or discard. Every promotion gets a `CHANGELOG.md` line.
- **Monthly opinion court:** re-argue three opinions with fresh evidence. Promote, demote, or reverse in `decisions/`.
- **Monthly mystery shopper:** an agent plays a customer through a whole lifecycle against the canon. Worst stage becomes the priority.
- **On every PR:** lexicon check, adapters fresh, every moment has an eval.

## Who this is built on

Will Guidara, Danny Meyer, Isadore Sharp, the Ritz-Carlton Gold Standards, the Heath brothers, Joey Coleman, Chris Voss, the Effortless Experience as the counterweight, Eli Weiss for the contemporary voice, and the public support handbooks of teams that write theirs down. The full list with what we took from each is in `sources/BIBLIOGRAPHY.md`.

## Contributing

See `CONTRIBUTING.md`. Opinions are meant to be argued. They're not meant to be vague.

MIT.
