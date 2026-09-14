# Setup by host

One canon, installed the way each tool expects. Every page ends the same way: connect the context layer, add your overlay, run the proof.

| Host | Page | Install |
|---|---|---|
| Claude Code | [claude-code.md](claude-code.md) | `/plugin marketplace add scmancillas/front-of-house` then `/plugin install front-of-house@front-of-house` |
| Codex CLI | [codex.md](codex.md) | `npx skills add scmancillas/front-of-house -g -a codex` |
| Cursor | [cursor.md](cursor.md) | `npx skills add scmancillas/front-of-house -g -a cursor` or copy `adapters/cursor/*.mdc` |
| OpenAI (custom GPT, Assistants, Agents SDK) | [openai.md](openai.md) | `adapters/openai-custom-gpt.txt` + upload the canon as knowledge |
| Gemini CLI | [gemini-cli.md](gemini-cli.md) | `gemini extensions install https://github.com/scmancillas/front-of-house` |
| GitHub Copilot | [copilot.md](copilot.md) | `npx skills add scmancillas/front-of-house -g -a github-copilot` + `adapters/copilot-instructions.md` |
| Windsurf, Cline, Continue, OpenCode, Goose, Roo, and 70+ others | [other-hosts.md](other-hosts.md) | `npx skills add scmancillas/front-of-house -g` |
| Anything with a system prompt (Slack bot, Intercom, Sierra, your own harness) | [generic.md](generic.md) | `adapters/system-prompt.txt` |
| The context layer (MCP), all hosts | [context-layer.md](context-layer.md) | one snippet per host |

If you're an AI agent doing the install, `AGENTS.md` at the repo root is written for you.
