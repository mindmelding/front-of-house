# Claude Code

**Plugin (recommended, auto-updates):**

```
/plugin marketplace add scmancillas/front-of-house
/plugin install front-of-house@front-of-house
```

The plugin's skill is the repo root, so the whole canon comes along and the moment playbooks load on demand. Update with `claude plugin update front-of-house@front-of-house`.

**Agent Skills CLI (same result, no marketplace):**

```
npx skills add scmancillas/front-of-house -g -a claude-code
```

**Manual (developer, stays in sync with your working tree):**

```
git clone https://github.com/scmancillas/front-of-house.git
ln -s "$(pwd)/front-of-house" ~/.claude/skills/front-of-house
```

Or per project: `scripts/install.sh claude <project-dir>` writes `CLAUDE.md` and links the moments as skills.

**Context layer:**

```
claude mcp add --transport http moonbase https://yavin.moonbase.ai/mcp \
  --header "Authorization: Bearer $MOONBASE_MCP_KEY"
```

**Overlay:** copy `overlay/*.template.md` into your project's `overlay/` and fill them in. Until `authority.md` grants something, every sensitive action is a nudge.

**Proof:** paste a real thread and ask for a reply. It should call `ask_account` before drafting. Then `python3 scripts/fohcheck.py` on the draft.
