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
case "$TOOL" in
  cursor)
    mkdir -p "$TARGET/.cursor/rules"
    cp "$HERE"/adapters/cursor/*.mdc "$TARGET/.cursor/rules/"
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
    cp "$HERE/adapters/CLAUDE.md" "$TARGET/.windsurf/rules/front-of-house.md"; echo "wrote $TARGET/.windsurf/rules/front-of-house.md"
    ;;
  cline)
    mkdir -p "$TARGET/.clinerules"
    cp "$HERE/adapters/CLAUDE.md" "$TARGET/.clinerules/front-of-house.md"; echo "wrote $TARGET/.clinerules/front-of-house.md"
    ;;
  generic)
    cp "$HERE/adapters/system-prompt.txt" "$TARGET/front-of-house.system-prompt.txt"; echo "wrote $TARGET/front-of-house.system-prompt.txt (paste as the system prompt, append your overlay)"
    ;;
  *) echo "unknown tool: $TOOL (cursor|claude|codex|gemini|copilot|windsurf|cline|generic)"; exit 2 ;;
esac
mkdir -p "$TARGET/overlay"
for t in "$HERE"/overlay/*.template.md; do
  dest="$TARGET/overlay/$(basename "${t%.template.md}").md"
  [[ -f "$dest" ]] || cp "$t" "$dest"
done
echo "overlay templates in $TARGET/overlay/ (fill these in; they never go in the canon)"
