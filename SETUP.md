# Setup: point a tool at Front of House

Three layers, loaded in this order:

1. **The canon** (this repo): who the agent is, how it sounds, what it never does.
2. **Your overlay** (private, git-ignored `overlay/`): your policies, authority grants, people, product.
3. **Your context layer** (a CRM or context graph reached over MCP): who the customer is, what we owe them, what they said.

The canon tells the agent *to* read the customer's file before speaking (`context/CONTRACT.md`). The context layer is *how* it reads it. Without layer 3 the agent still behaves well; it just treats every conversation as a first one and says so.

## Install, by host

| Host | Install |
|---|---|
| **Claude Code** (recommended, auto-updates) | `/plugin marketplace add scmancillas/front-of-house` then `/plugin install front-of-house@front-of-house` |
| **Codex, Cursor, Copilot, Gemini CLI, Windsurf, Cline, OpenCode, and 70+ [Agent Skills](https://agentskills.io) hosts** | `npx skills add scmancillas/front-of-house -g` (add `-a codex`, `-a cursor`, etc. to target one) |
| **Gemini CLI** (extension) | `gemini extensions install https://github.com/scmancillas/front-of-house` |
| **OpenAI custom GPT / Assistants / Agents SDK** | `adapters/openai-custom-gpt.txt` or `adapters/system-prompt.txt` |
| **Anything with a system prompt** | `adapters/system-prompt.txt` |
| **Manual, per project** | `scripts/install.sh <cursor|claude|codex|gemini|copilot|windsurf|cline|generic> <project-dir>` |

Per-host walkthroughs, including the MCP context layer for each: [`docs/setup/`](docs/setup/README.md).

Every host ends the same way: connect the context layer, add your overlay, run the proof on one real thread.

---

## What the agent does with all this, in order

1. Loads the mindset and precedence (always).
2. Reads the customer's file through the context tools. If none are connected, says so internally and proceeds as a first conversation.
3. Picks one moment playbook.
4. Reads the overlay for policy, authority, and people.
5. Drafts in the voice, checks against the lexicon.
6. Nudges before anything sensitive. Acts only inside a grant.
7. Replies. Writes the touch note back.
