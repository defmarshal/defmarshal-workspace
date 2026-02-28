#!/usr/bin/env bash
set -euo pipefail
# Initialize missing agent log files with a placeholder entry.
# This helps health checks detect presence even if the agent hasn't run yet.

WORKSPACE="/home/ubuntu/.openclaw/workspace"
AGENTS=(
  "linkedin-pa-agent"
  "research-agent"
  "content-agent"
  "dev-agent"
  "supervisor"
  "agent-manager"
  "meta-agent"
)

for agent in "${AGENTS[@]}"; do
  LOG="$WORKSPACE/memory/$agent.log"
  if [ ! -f "$LOG" ]; then
    echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Log initialized (placeholder)" > "$LOG"
    echo "Created placeholder for $agent"
  fi
done
