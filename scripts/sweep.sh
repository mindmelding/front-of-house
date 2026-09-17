#!/bin/bash
# Front of House sweep runner. Scheduled by the OS (ops/launchd.template.plist), or run by hand.
# Reads engine/SWEEP.md into a non-interactive agent run, writes the heartbeat, never asks, never sends.
#
#   scripts/sweep.sh                 run once now
#   FOH_OVERLAY=... scripts/sweep.sh use a specific overlay
#
# Requires: the `claude` CLI on PATH (or CLAUDE_BIN), and overlay/mcp.json pointing at the context source.
# The sweep only ever needs: Read, Write, Edit, Bash for scripts/*, and the context connector's tools.
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$HOME/.nvm/versions/node/v22.19.0/bin:$PATH"
export HOME="${HOME:-$(cd ~ && pwd)}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
OVERLAY="${FOH_OVERLAY:-$ROOT/overlay}"
export FOH_OVERLAY="$OVERLAY"
LOG_DIR="$OVERLAY/logs"; mkdir -p "$LOG_DIR" "$OVERLAY/state" "$OVERLAY/briefs"
LOG="$LOG_DIR/sweep-$(date +%Y-%m-%d).log"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
TIMEOUT_SECS="${SWEEP_TIMEOUT:-1500}"
MCP_ARGS=()
[[ -f "$OVERLAY/mcp.json" ]] && MCP_ARGS=(--mcp-config "$OVERLAY/mcp.json")
[[ -f "$OVERLAY/secrets.env" ]] && set -a && . "$OVERLAY/secrets.env" && set +a

log() { echo "[$(date -Iseconds)] $*" | tee -a "$LOG"; }

log "=== sweep start (overlay $OVERLAY) ==="
python3 scripts/engine.py heartbeat start >> "$LOG" 2>&1
python3 scripts/engine.py house init >> "$LOG" 2>&1

PROMPT="Follow $ROOT/engine/SWEEP.md exactly, top to bottom, as the scheduled sweep. Working directory is $ROOT; the overlay is $OVERLAY. Ask no questions. Send nothing. Register every account and person with scripts/engine.py alias add before writing anything derived from them. End with scripts/engine.py heartbeat end --signal and one line starting SWEEP DONE: or SWEEP PARTIAL:. ${1:-}"

if timeout "$TIMEOUT_SECS" "$CLAUDE_BIN" -p "$PROMPT" \
    --output-format text --strict-mcp-config \
    --permission-mode acceptEdits \
    --allowedTools "Read,Write,Edit,Glob,Grep,Bash(python3 scripts/*),Bash(python3 $ROOT/scripts/*),Bash(cat *),Bash(ls *),mcp__moonbase__*" \
    "${MCP_ARGS[@]}" < /dev/null >> "$LOG" 2>&1; then
  log "agent exited 0"
else
  rc=$?
  log "WARN agent exited $rc"
fi

# If the agent did not close the heartbeat, close it as a failure so the hook can see it.
python3 - "$OVERLAY" <<'PY' >> "$LOG" 2>&1
import json, sys, datetime as dt, pathlib
p = pathlib.Path(sys.argv[1]) / "state" / "heartbeat.json"
h = json.loads(p.read_text()) if p.exists() else {}
if not h.get("ended"):
    h["ended"] = dt.datetime.now().isoformat(timespec="seconds"); h["signal"] = "FAILED: agent did not close the heartbeat"
    p.write_text(json.dumps(h, indent=2) + "\n"); print("heartbeat closed as FAILED")
PY
python3 scripts/engine.py alias audit >> "$LOG" 2>&1 || log "WARN alias audit found leaks; see log"
tail -n 3 "$LOG"
