#!/usr/bin/env bash
set -euo pipefail
# Run an OpenClaw agent with a given message

WORKSPACE="/home/ubuntu/.openclaw/workspace"

usage() {
  echo "Usage: quick run-agent <agent-id> <message>"
  echo "Example: quick run-agent main 'You are the research-agent...'"
  exit 1
}

if [ $# -lt 2 ]; then
  usage
fi

AGENT_ID="$1"
shift
MESSAGE="$*"

openclaw agent --agent "$AGENT_ID" --message "$MESSAGE" --thinking low --timeout 300
