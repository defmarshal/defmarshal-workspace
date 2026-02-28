#!/usr/bin/env bash
set -euo pipefail
# Check and ensure agent log files exist in memory/

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory"

echo "Agent Log Health Check"
echo "----------------------"

AGENTS=(
  "linkedin-pa-agent"
  "research-agent"
  "content-agent"
  "dev-agent"
  "supervisor"
  "agent-manager"
  "meta-agent"
)

missing=0
for agent in "${AGENTS[@]}"; do
  logfile="$LOG_DIR/$agent.log"
  if [ -f "$logfile" ]; then
    # Check if file has recent activity (within last 24h)
    if [ $(find "$logfile" -mmin -1440 2>/dev/null | wc -l) -gt 0 ]; then
      echo "✅ $agent.log exists (recent activity)"
    else
      echo "⚠️  $agent.log exists but stale (no activity in 24h)"
    fi
  else
    echo "❌ $agent.log missing"
    missing=$((missing+1))
  fi
done

echo
if [ $missing -eq 0 ]; then
  echo "✅ All agent logs present."
else
  echo "⚠️  $missing agent log(s) missing."
  echo "   Logs are created automatically when agents run."
fi
