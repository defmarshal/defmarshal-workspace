#!/usr/bin/env bash
set -euo pipefail
# List expected agent log files that are missing

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory"

echo "Missing Agent Logs Check"
echo "-----------------------"

# Expected agent log filenames
expected=(
  "linkedin-pa-agent.log"
  "research-agent.log"
  "content-agent.log"
  "dev-agent.log"
  "supervisor.log"
  "agent-manager.log"
  "meta-agent.log"
  "cron-supervisor.log"
  "gateway-watchdog.log"
)

missing=0
for log in "${expected[@]}"; do
  if [ ! -f "$LOG_DIR/$log" ]; then
    echo "❌ Missing: $log"
    missing=$((missing+1))
  else
    echo "✅ Present: $log"
  fi
done

echo
if [ $missing -eq 0 ]; then
  echo "All expected agent logs are present."
else
  echo "⚠️  $missing log file(s) missing. Some agents may not have run yet or are using alternative logging."
fi
