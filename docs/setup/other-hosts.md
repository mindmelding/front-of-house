# Windsurf, Cline, Continue, OpenCode, Goose, Roo, Aider, and the rest

Anything that speaks the open [Agent Skills](https://agentskills.io) format:

```
npx skills add scmancillas/front-of-house -g
```

`-g` installs for your user across projects; drop it to install into the current project. Target a specific host with `-a windsurf`, `-a cline`, `-a opencode`, and so on (`npx skills add --help` lists them). Update with `npx skills update front-of-house -g`.

If the host has a rules or instructions file and no skill support, use the generated files:

| Host | File to drop in |
|---|---|
| Windsurf | `.windsurf/rules/front-of-house.md` from `adapters/CLAUDE.md` |
| Cline | `.clinerules/front-of-house.md` from `adapters/CLAUDE.md` |
| Continue | a rule block in `.continue/` from `adapters/system-prompt.txt` |
| Anything else | `adapters/system-prompt.txt` wherever the system prompt goes |

**Context layer:** every one of these that supports MCP takes the same server: `https://yavin.moonbase.ai/mcp` with an `Authorization: Bearer $MOONBASE_MCP_KEY` header. See `context-layer.md`.

**Overlay and proof:** same as every host.
