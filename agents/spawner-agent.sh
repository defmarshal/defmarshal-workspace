#!/usr/bin/env bash
# Spawner Agent — Spawns another OpenClaw agent with a given task.
# Usage: agents/spawner-agent.sh <agent-id> <task>
# Example: agents/spawner-agent.sh content-agent "Quick check"

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

if [ $# -lt 2 ]; then
  echo "Usage: $0 <agent-id> <task>"
  echo "Example: $0 content-agent \"Quick check\""
  exit 1
fi

AGENT_ID="$1"
shift
TASK="$*"

echo "Spawning agent '$AGENT_ID' with task: $TASK"
openclaw agents spawn --agent-id "$AGENT_ID" --task "$TASK" --timeout-seconds 600
