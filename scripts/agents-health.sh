#!/usr/bin/env bash
# Show health summary of all OpenClaw agents

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "OpenClaw Agents Health"
echo "----------------------"

# Check gateway
if systemctl --user is-active openclaw-gateway.service &>/dev/null; then
  echo "Gateway: ✅ running"
else
  echo "Gateway: ❌ inactive"
fi

# List agent logs to find last run
echo
echo "Recent agent activity:"
for agent in research-agent content-agent dev-agent idea-executor meta-agent workspace-builder notifier-agent torrent-bot agni vishwakarma; do
  log="$WORKSPACE/$agent.log"
  if [ -f "$log" ]; then
    last=$(tail -1 "$log" | awk '{print $1, $2}' 2>/dev/null)
    if [ -n "$last" ]; then
      echo "  $agent: $last"
    else
      echo "  $agent: (no log entries)"
    fi
  else
    echo "  $agent: (no log file)"
  fi
done

# Show cron status
echo
echo "Cron jobs (via openclaw):"
openclaw cron list 2>/dev/null | grep -E "ok|error" | head -5 | sed 's/^/  /'
