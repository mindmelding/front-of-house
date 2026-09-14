# Gemini CLI

**Extension:**

```
gemini extensions install https://github.com/scmancillas/front-of-house
```

The extension's context file is the generated `GEMINI.md` at the repo root. It declares the Moonbase context layer as an MCP server and asks for `MOONBASE_MCP_KEY` as a sensitive setting on install. If your Gemini CLI version doesn't accept `httpUrl` servers inside an extension, add the server to `~/.gemini/settings.json` instead:

```json
{
  "mcpServers": {
    "moonbase": {
      "httpUrl": "https://yavin.moonbase.ai/mcp",
      "headers": { "Authorization": "Bearer $MOONBASE_MCP_KEY" }
    }
  }
}
```

Confirm with `gemini extensions list` and `/mcp` inside a session.

**Agent Skills CLI works too:** `npx skills add scmancillas/front-of-house -g -a gemini-cli`.

**Overlay and proof:** same as every host.
