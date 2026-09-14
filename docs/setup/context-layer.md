# The context layer, per host

Front of House reads the customer's file before it speaks. The file lives in a context layer reached over MCP. The reference is Moonbase: endpoint `https://yavin.moonbase.ai/mcp`, bearer key starting `mb_`, tools `ask_account`, `list_events`, `get_event`, `list_accounts`. Keep the key in an environment variable named `MOONBASE_MCP_KEY`; never commit it.

| Host | Where | Snippet |
|---|---|---|
| Claude Code | CLI | `claude mcp add --transport http moonbase https://yavin.moonbase.ai/mcp --header "Authorization: Bearer $MOONBASE_MCP_KEY"` |
| Codex CLI | `~/.codex/config.toml` | `adapters/codex-config.toml` (`url` + `bearer_token_env_var`) |
| Cursor | `.cursor/mcp.json` | `overlay/mcp.template.json` (`url` + `headers`) |
| Gemini CLI | extension or `~/.gemini/settings.json` | `httpUrl` + `headers` |
| VS Code / Copilot agent mode | `.vscode/mcp.json` | `type: http`, `url`, `headers` |
| Windsurf, Cline, OpenCode, Goose | their MCP config | same `url` + `Authorization` header |
| OpenAI Agents SDK | code | attach the MCP server with the bearer header |
| Custom GPT | Actions | front the REST API with an Action, or paste the file into the chat |

**Another CRM or context graph?** Copy `context/adapters/TEMPLATE.md`, map each contract row to a call, declare what the agent may write back, run `make build`. A Cursor rule for it is generated automatically.

**No context layer?** The agent still works. It treats every conversation as a first one, says so internally, and writes the file as it goes. It never pretends to know.
