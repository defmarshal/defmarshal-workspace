#!/usr/bin/env bash
# Spawner Agent — Spawns another OpenClaw agent with a given task.
# Usage: agents/spawner-agent.sh <agent-id> <task>
# Example: agents/spawner-agent.sh main "You are the content-agent. Create a daily digest."

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

if [ $# -lt 2 ]; then
  echo "Usage: $0 <agent-id> <task>"
  echo "Example: $0 main \"You are the content-agent. Create a daily digest.\""
  exit 1
fi

AGENT_ID="$1"
shift
TASK="$*"

echo "Spawning agent '$AGENT_ID' with task: $TASK"
openclaw agent \
  --agent "$AGENT_ID" \
  --message "$TASK" \
  --thinking low \
  --timeout 600000
