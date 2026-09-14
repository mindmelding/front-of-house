#!/usr/bin/env bash
# Install Front of House into a project for a given tool.
#   scripts/install.sh cursor /path/to/project
#   scripts/install.sh claude /path/to/project
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="${1:-}"; TARGET="${2:-}"
if [[ -z "$TOOL" || -z "$TARGET" ]]; then echo "usage: $0 <cursor|claude> <project-dir>"; exit 2; fi
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
    for d in "$HERE"/moments/*/; do
      n="$(basename "$d")"; ln -sfn "$d" "$TARGET/.claude/skills/foh-$n"
    done
    echo "linked $(ls -d "$HERE"/moments/*/ | wc -l | tr -d ' ') moment skills into $TARGET/.claude/skills/"
    echo "context layer: claude mcp add --transport http moonbase https://yavin.moonbase.ai/mcp --header \"Authorization: Bearer \$MOONBASE_MCP_KEY\""
    ;;
  *) echo "unknown tool: $TOOL (cursor|claude)"; exit 2 ;;
esac
mkdir -p "$TARGET/overlay"
for t in "$HERE"/overlay/*.template.md; do
  dest="$TARGET/overlay/$(basename "${t%.template.md}").md"
  [[ -f "$dest" ]] || cp "$t" "$dest"
done
echo "overlay templates in $TARGET/overlay/ (fill these in; they never go in the canon)"
