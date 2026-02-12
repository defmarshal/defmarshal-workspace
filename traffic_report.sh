#!/bin/bash
# Traffic report – runs daily at 5 AM Jakarta time (22:00 UTC)
REPORT_TIME=$(date '+%Y-%m-%d %H:%M')

# Get traffic for both routes (toll-free)
PARUNG_TEBET=$(python3 /home/ubuntu/.openclaw/workspace/traffic_route "Parung, Bogor" "Tebet, Jakarta" 2>/dev/null)
TEBET_KELAPAGADING=$(python3 /home/ubuntu/.openclaw/workspace/traffic_route "Tebet, Jakarta" "Kelapa Gading, Jakarta" 2>/dev/null)

MSG="Traffic report for $REPORT_TIME (toll‑free routes)

* Parung → Tebet:*
$PARUNG_TEBET

* Tebet → Kelapa Gading:*
$TEBET_KELAPAGADING

Stay safe on the road!"

echo "$MSG"
openclaw message send --target telegram:952170974 --message "$MSG"
