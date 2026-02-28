#!/usr/bin/env bash
# Tail recent lines from agent logs
# Usage: quick log-tail [agent|all] [lines]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORY="$WORKSPACE/memory"

TARGET="${1:-all}"
LINES="${2:-30}"

AGENTS=(dev-agent content-agent research-agent meta-agent idea-executor idea-generator supervisor agent-manager)

tail_log() {
  local name="$1"
  local file="$MEMORY/${name}.log"
  if [[ -f "$file" ]]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📋 ${name}.log (last ${LINES} lines)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tail -n "$LINES" "$file"
    echo ""
  else
    echo "  ⚠️  ${name}.log not found"
  fi
}

if [[ "$TARGET" == "all" ]]; then
  for agent in "${AGENTS[@]}"; do
    tail_log "$agent"
  done
else
  tail_log "$TARGET"
fi
