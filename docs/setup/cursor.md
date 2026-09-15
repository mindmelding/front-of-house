# Cursor

**Rules (either path):**

```
npx skills add scmancillas/front-of-house -g -a cursor
```

or copy the generated rules directly:

```
scripts/install.sh cursor /path/to/project
```

That puts 15 rules in `.cursor/rules/` and stamps the canon's absolute path into the always-on rule so the agent can find `scripts/shift.py` and `FIRST-SHIFT.md` from your project. The rules are: `front-of-house.mdc` (always on), `front-of-house-voice.mdc`, `context-moonbase.mdc`, and one `moment-*.mdc` per playbook, all agent-requested by description. Invoke one by name with `@moment-angry-customer`.

**Context layer:** `.cursor/mcp.json` (template in `overlay/mcp.template.json`):

```json
{
  "mcpServers": {
    "moonbase": {
      "url": "https://yavin.moonbase.ai/mcp",
      "headers": { "Authorization": "Bearer ${env:MOONBASE_MCP_KEY}" }
    }
  }
}
```

Restart Cursor and confirm the four Moonbase tools appear under Settings, MCP.

**Overlay:** the installer creates `overlay/` in the project and points the always-on rule at it. If you used `npx skills` instead, add `Overlay: read ./overlay/*.md before replying.` to the top of `front-of-house.mdc`.

**Already have a Moonbase server in `~/.cursor/mcp.json`?** Delete the project-level `.cursor/mcp.json` the installer wrote; the tool names are the same whatever the server is called.

**Test it:** open the project in Cursor, start a new Agent chat, and say `read FIRST-SHIFT.md and run it`. It should list the connectors it found and propose one, nudge before reading it, ask the interview one question at a time (mostly as confirmations), offer a time window, and come back with a brief.

**Proof:** "Using Front of House, reply to this message from Dana. Read her file first." It must call the context tools before drafting.

**Or let Cursor do all of this:** clone the repo and say "read AGENTS.md and follow it to set yourself up in this project." It will stop to ask you for the key and for permission to write the MCP config.
