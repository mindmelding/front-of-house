# Codex CLI

**Install the skill:**

```
npx skills add scmancillas/front-of-house -g -a codex
```

Codex also reads `AGENTS.md` in the working directory. If you'd rather not install a skill, copy `adapters/AGENTS.md` into the project as `AGENTS.md` (or append it to an existing one). The repo's own root `AGENTS.md` is an install bootstrap, not the behavior file; use the one in `adapters/`.

**Context layer:** add to `~/.codex/config.toml` (the snippet is in `adapters/codex-config.toml`):

```toml
[mcp_servers.moonbase]
url = "https://yavin.moonbase.ai/mcp"
bearer_token_env_var = "MOONBASE_MCP_KEY"
```

Or `codex mcp add moonbase --url https://yavin.moonbase.ai/mcp`, then add the `bearer_token_env_var` line by hand. Set `MOONBASE_MCP_KEY` in your shell.

**Overlay and proof:** same as every host. Copy `overlay/*.template.md` into the project, fill in authority and policies, then paste a real thread and check the reply read the file first.
