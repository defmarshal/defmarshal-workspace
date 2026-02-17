#!/usr/bin/env bash
# Spawner Agent — Spawns another OpenClaw agent with a given task.
# Supports one-shot or daemon (loop) mode for permanent 24/7 agents.
# Usage:
#   agents/spawner-agent.sh <agent-id> <task>           # one-shot
#   agents/spawner-agent.sh <agent-id> <task> --daemon  # run as persistent daemon (24/7)
#
# Example: agents/spawner-agent.sh content-agent "Create daily digest" --daemon

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

if [ $# -lt 2 ]; then
  echo "Usage: $0 <agent-id> <task> [--daemon]"
  echo "Example (one-shot): $0 main \"Create a digest\""
  echo "Example (daemon):   $0 content-agent \"Daily cycle\" --daemon"
  exit 1
fi

AGENT_ID="$1"
shift

DAEMON=false
# Filter out --daemon flag from arguments and set DAEMON
FILTERED_ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--daemon" ]]; then
    DAEMON=true
  else
    FILTERED_ARGS+=("$arg")
  fi
done

if [ ${#FILTERED_ARGS[@]} -eq 0 ]; then
  echo "Error: missing task"
  exit 1
fi

TASK="${FILTERED_ARGS[*]}"

if [ "$DAEMON" = false ]; then
  echo "Spawning agent '$AGENT_ID' with task: $TASK"
  openclaw agent --agent "$AGENT_ID" --message "$TASK" --thinking low --timeout 600000
else
  echo "Starting daemon for agent '$AGENT_ID' with task: $TASK"
  echo "Press Ctrl+C to stop."
  while true; do
    # Quiet hours check removed 2026-02-17; run 24/7
    if ! openclaw sessions list --json 2>/dev/null | grep -q "\"label\":\"$AGENT_ID\""; then
      echo "$(TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M') Spawning $AGENT_ID..."
      openclaw agent --agent "$AGENT_ID" --message "$TASK" --thinking low --timeout 600000 || true
      sleep 5
    else
      echo "$(TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M') $AGENT_ID already running, sleeping..."
      sleep 30
    fi
  done
fi