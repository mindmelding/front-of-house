---
id: first-shift-discover
type: process
status: active
last_reviewed: 2026-09-15
---

# Discover: look before you ask

A new hire who asks the manager "so, what do we sell?" on day one didn't read the menu. Before the interview, the agent reads everything on the operator's machine that answers the questions it would otherwise ask. `python3 scripts/shift.py discover` does the inventory; this file says what to do with it.

## What the script finds

**Connectors.** Every MCP server configured for every host it knows (Cursor global and project, Claude Code user and project, Claude Desktop, Codex, Gemini CLI, VS Code, Windsurf, Cline), grouped by family:

| Family | Examples | What it's good for |
|---|---|---|
| customer context / CRM | a CRM, a context graph, an account database | the customer's file: promises, people, outcomes, history. Best source when present. |
| support desk | ticketing and shared-inbox tools | the threads themselves, open and closed |
| conversations | Slack, email, chat connectors | where customers actually write, and the operator's own voice |
| meetings | call recorders and note-takers | what customers said out loud, desired outcomes in their words |
| product usage | analytics | first value, silence, milestones |
| billing | payment platforms | who's paying, plan changes, refunds already given |
| work tracking | issue trackers, docs | what we owe engineering-side, feature requests already filed |

Secrets are masked before anything is written. `overlay/discovery.md` is local and never leaves the overlay.

**Local files.** Project instructions (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `README.md`, `.cursor/rules`), user-level instructions, agent memory indexes, and folders named `docs`, `kb`, `knowledge`, `context`, `notes`, `customers`, `playbooks`. These usually say who the operator is, what the company does, who it sells to, and which accounts matter this month.

## What the agent does with it

1. **Read the local files.** All of them, quickly. Take notes against the interview keys: operator name and sign-off, company one-liner, who they sell to, channels, escalation people, policies, first value, recurring issues, accounts under watch. Every key you can fill from disk becomes a confirmation instead of a question.
2. **Pick the customer's file.** Rank the connectors: a CRM or context graph first, then a support desk, then a shared inbox. If two are present, say which does what ("the CRM for the file, the meeting notes for what they said, the inbox for voice"). If the memory or docs say one is being sunset, don't recommend it.
3. **Say it back in four lines.** What you found, what you'd use, what you're unsure of. One question: "Use that, or point me somewhere else?"
4. **Nothing found?** Ask where customer context lives: "A CRM, a support desk, a shared inbox, a folder of notes, a spreadsheet?" Then help wire it (`docs/setup/context-layer.md`), or work from files the operator drops in `overlay/`. Never name a specific vendor as the expected answer.

## Customer identification

Not everyone in the conversation history is a customer. Before the dig, the agent needs a rule for who counts.

Ask once: "Do you have a way to tell customers from prospects, vendors, and teammates? A stage field, a plan, a list?"

- **Yes:** record the rule in `overlay/customers.md` (field and values, or the list's location). Done.
- **No, or "take a guess":** do a quick pass over the roster and propose heuristics, in order of confidence, into `overlay/customers.md`. Starting points:
  - a paying plan or an active subscription in billing
  - an account object with a lifecycle stage past "prospect"
  - a sender domain that isn't ours and isn't a known vendor
  - a thread attached to an account with a signed date
  - recurring senders over the window who ask "how do I," "it broke," or "can you"
  Show the operator the rule and the accounts it's unsure about. Ask for a yes. Refine as the journal grows; a rule that misfires twice gets rewritten.

Vendors, investors, candidates, and teammates get their own line in `overlay/customers.md` so the agent never drafts a customer reply to the payroll provider.

## What discovery never does

It never sends anything anywhere. It never reads a key's value, only that a server exists. It never opens a connector; that's the dig, and the dig is nudged. It never assumes a connector is the right one because it's the only one.
