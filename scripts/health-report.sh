#!/usr/bin/env bash
# Comprehensive health report — single view of system status

WORKSPACE="/home/ubuntu/.openclaw/workspace"

echo "🖥️  System Health Report"
echo "-----------------------"

# Time & uptime
echo "📅 $(date -u '+%Y-%m-%d %H:%M UTC')"
[ -f /proc/uptime ] && echo "⏱️  Uptime: $(awk '{print int($1/3600)"h"}' /proc/uptime)"
echo

# Disk
echo "💾 Disk Usage (workspace):"
df -h "$WORKSPACE" | tail -1 | awk '{print "  Used: "$5" ("$3"/"$2"), Free: "$4}'
echo

# Gateway
echo "🌐 Gateway:"
if openclaw gateway status >/dev/null 2>&1; then
  echo "  ✅ Running (port 18789)"
else
  echo "  ❌ Not responding"
fi
echo

# Updates
echo "🔧 System Updates:"
if command -v apt-get &>/dev/null; then
  if PENDING=$(apt-get -s upgrade 2>&1 | grep -c '^Inst' 2>/dev/null); then
    :
  else
    PENDING=0
  fi
  if [ "${PENDING:-0}" -gt 0 ]; then
    echo "  ⚠️  $PENDING packages pending"
  else
    echo "  ✅ All up to date"
  fi
else
  echo "  ⚠️  apt-get not available"
fi
echo

# Agents
echo "🤖 Agents (last 24h):"
bash "$WORKSPACE/scripts/agents-health-improved.sh" 2>/dev/null | sed -n '2,$p' | head -7
echo

# Downloads
echo "📥 Active Downloads (aria2):"
if command -v aria2c &>/dev/null; then
  DOWNLOADS=$(aria2c --rpc-listen-port=6800 --enable-rpc --rpc-allow-origin-all -s1 2>/dev/null | grep -c 'Active\|Waiting' || echo 0)
  echo "  $DOWNLOADS active/downloading"
else
  echo "  aria2 not available"
fi
echo

# Memory
echo "🧠 Memory:"
free -h | awk '/Mem:/ {print "  RAM: "$7" free / "$2" ("$3"/"$2" used)"}'
echo

echo "✅ Report generated. Use './quick health-report' to run."
