#!/usr/bin/env bash
# Install Front of House into a project for a given tool.
#   scripts/install.sh cursor /path/to/project
#   scripts/install.sh claude /path/to/project
#   also: codex | gemini | copilot | windsurf | cline | generic
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="${1:-}"; TARGET="${2:-}"
if [[ -z "$TOOL" || -z "$TARGET" ]]; then echo "usage: $0 <cursor|claude|codex|gemini|copilot|windsurf|cline|generic> <project-dir>"; exit 2; fi
mkdir -p "$TARGET"
# Insert a "where the canon lives" block right after the frontmatter of a rules file,
# so relative paths in the rules (scripts/, FIRST-SHIFT.md, moments/) resolve for the agent.
stamp_canon() {
  local f="$1"
  python3 - "$f" "$HERE" "$TARGET" <<'PY'
import sys
f, canon, target = sys.argv[1:4]
s = open(f).read()
block = (f"**Where things live.** The Front of House canon is at `{canon}`. Every relative path in these rules "
         f"(`scripts/shift.py`, `FIRST-SHIFT.md`, `moments/`, `guardrails/`, `first-shift/`) resolves there. "
         f"The private overlay for this project is `{target}/overlay/`; run shift.py from this project root so it finds it. "
         f"First message of a new session: run `python3 {canon}/scripts/shift.py status --brief` and act on it.\n\n")
if "**Where things live.**" in s: sys.exit(0)
if s.startswith("---"):
    end = s.index("\n---", 3) + 4
    s = s[:end] + "\n" + block + s[end:].lstrip("\n")
else:
    s = block + s
open(f, "w").write(s)
PY
}
case "$TOOL" in
  cursor)
    mkdir -p "$TARGET/.cursor/rules"
    cp "$HERE"/adapters/cursor/*.mdc "$TARGET/.cursor/rules/"
    stamp_canon "$TARGET/.cursor/rules/front-of-house.mdc"
    if [[ ! -f "$TARGET/.cursor/mcp.json" ]]; then
      cp "$HERE/overlay/mcp.template.json" "$TARGET/.cursor/mcp.json"
      echo "wrote $TARGET/.cursor/mcp.json (set MOONBASE_MCP_KEY in your environment, or edit the file)"
    else
      echo "kept existing $TARGET/.cursor/mcp.json; add the moonbase server from overlay/mcp.template.json if needed"
    fi
    echo "installed $(ls "$HERE"/adapters/cursor/*.mdc | wc -l | tr -d ' ') rules into $TARGET/.cursor/rules/"
    ;;
  claude)
    mkdir -p "$TARGET/.claude/skills"
    if [[ -f "$TARGET/CLAUDE.md" ]]; then
      printf '\n\n# Front of House\nCanon at %s. Read its MINDSET.md and PRECEDENCE.md before any customer-facing work and follow its loading rules (adapters/CLAUDE.md).\n' "$HERE" >> "$TARGET/CLAUDE.md"
      echo "appended pointer to existing $TARGET/CLAUDE.md"
    else
      cp "$HERE/adapters/CLAUDE.md" "$TARGET/CLAUDE.md"
      echo "wrote $TARGET/CLAUDE.md"
    fi
    ln -sfn "$HERE" "$TARGET/.claude/skills/front-of-house"
    echo "linked the canon as one skill at $TARGET/.claude/skills/front-of-house (playbooks load on demand from inside it)"
    echo "context layer: claude mcp add --transport http moonbase https://yavin.moonbase.ai/mcp --header \"Authorization: Bearer \$MOONBASE_MCP_KEY\""
    ;;
  codex)
    if [[ -f "$TARGET/AGENTS.md" ]]; then
      printf '\n\n# Front of House\nCanon at %s. Read its MINDSET.md and PRECEDENCE.md before any customer-facing work and follow the loading rules in adapters/AGENTS.md.\n' "$HERE" >> "$TARGET/AGENTS.md"
      echo "appended pointer to existing $TARGET/AGENTS.md"
    else
      cp "$HERE/adapters/AGENTS.md" "$TARGET/AGENTS.md"; echo "wrote $TARGET/AGENTS.md"
    fi
    echo "context layer: add adapters/codex-config.toml to ~/.codex/config.toml and set MOONBASE_MCP_KEY"
    ;;
  gemini)
    cp "$HERE/GEMINI.md" "$TARGET/GEMINI.md"; echo "wrote $TARGET/GEMINI.md"
    echo "or install the extension: gemini extensions install https://github.com/scmancillas/front-of-house"
    ;;
  copilot)
    mkdir -p "$TARGET/.github"
    cp "$HERE/adapters/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"; echo "wrote $TARGET/.github/copilot-instructions.md"
    ;;
  windsurf)
    mkdir -p "$TARGET/.windsurf/rules"
    cp "$HERE/adapters/CLAUDE.md" "$TARGET/.windsurf/rules/front-of-house.md"; stamp_canon "$TARGET/.windsurf/rules/front-of-house.md"; echo "wrote $TARGET/.windsurf/rules/front-of-house.md"
    ;;
  cline)
    mkdir -p "$TARGET/.clinerules"
    cp "$HERE/adapters/CLAUDE.md" "$TARGET/.clinerules/front-of-house.md"; stamp_canon "$TARGET/.clinerules/front-of-house.md"; echo "wrote $TARGET/.clinerules/front-of-house.md"
    ;;
  generic)
    cp "$HERE/adapters/system-prompt.txt" "$TARGET/front-of-house.system-prompt.txt"; echo "wrote $TARGET/front-of-house.system-prompt.txt (paste as the system prompt, append your overlay)"
    ;;
  *) echo "unknown tool: $TOOL (cursor|claude|codex|gemini|copilot|windsurf|cline|generic)"; exit 2 ;;
esac
( cd "$TARGET" && FOH_OVERLAY="$TARGET/overlay" python3 "$HERE/scripts/shift.py" init --host "$TOOL" >/dev/null )
echo "overlay initialized at $TARGET/overlay/ (never goes in the canon). Next: tell the agent to read FIRST-SHIFT.md and run it."
