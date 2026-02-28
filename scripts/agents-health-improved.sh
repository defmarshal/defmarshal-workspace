#!/usr/bin/env bash
set -euo pipefail
# Show recent agent activity from memory logs with clearer timestamps

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "Recent Agent Activity (last 24h)"
echo "--------------------------------"

if ! command -v jq &>/dev/null; then
  echo "⚠️  jq not installed; install with: sudo apt-get install -y jq"
  exit 1
fi

# Get agent names from active-tasks or fallback to known list
AGENTS=$(jq -r '.tasks[].agent // empty' "$WORKSPACE/active-tasks.md" 2>/dev/null || cat <<'EOF'
linkedin-pa-agent
research-agent
content-agent
dev-agent
supervisor
agent-manager
meta-agent
EOF
)

NOW=$(date -u +%s)
ONE_DAY_AGO=$((NOW - 86400))

for agent in $AGENTS; do
  LOG="$WORKSPACE/memory/$agent.log"
  if [ -f "$LOG" ]; then
    # Find most recent timestamp within last 24h
    LAST_LINE=$(tail -1 "$LOG")
    if echo "$LAST_LINE" | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
      TS=$(echo "$LAST_LINE" | awk '{print $1" "$2}')
      TS_EPOCH=$(date -d "$TS" +%s 2>/dev/null || echo 0)
      if [ "$TS_EPOCH" -ge "$ONE_DAY_AGO" ]; then
        echo "✅ $agent: $TS"
      else
        echo "❌ $agent: last activity $TS (>24h ago)"
      fi
    else
      echo "⚠️  $agent: no timestamp found in log"
    fi
  else
    echo "❌ $agent: log file missing"
  fi
done

echo
echo "Gateway: $($WORKSPACE/quick gateway-status 2>/dev/null | head -1 || echo '⚠️  status unavailable')"
