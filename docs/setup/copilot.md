# GitHub Copilot

**Repository instructions:** copy `adapters/copilot-instructions.md` to `.github/copilot-instructions.md` in the project. Copilot reads it on every chat in that repo.

**Skill:**

```
npx skills add scmancillas/front-of-house -g -a github-copilot
```

**Context layer:** Copilot's MCP support varies by surface (VS Code agent mode supports MCP servers in `.vscode/mcp.json`):

```json
{
  "servers": {
    "moonbase": {
      "type": "http",
      "url": "https://yavin.moonbase.ai/mcp",
      "headers": { "Authorization": "Bearer ${MOONBASE_MCP_KEY}" }
    }
  }
}
```

**Overlay and proof:** same as every host.
