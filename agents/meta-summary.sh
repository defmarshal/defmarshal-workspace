#!/bin/bash
set -euo pipefail

# Ensure openclaw CLI is available in cron environment
export PATH="$HOME/.npm-global/bin:$PATH"

cd "/home/ubuntu/.openclaw/workspace"

# Gather metrics
DISK_PCT=$(df -h / | awk 'NR==2 {gsub(/%/,""); print $5}')
AGENTS=$(openclaw sessions --json 2>/dev/null | python3 -c "import json,sys; data=json.load(sys.stdin); print(len([s for s in data.get('sessions',[]) if s.get('status')=='running']))" || echo "?")
TODAY=$(date +%Y-%m-%d)
REPORTS=$(ls research/${TODAY}*.md 2>/dev/null | wc -l || echo 0)
UPDATES=$(apt list --upgradable 2>/dev/null | wc -l)

# Weather (Bogor) - using Open-Meteo API
WEATHER=$(curl -s 'https://api.open-meteo.com/v1/forecast?latitude=-6.5963&longitude=106.7972&current_weather=true&temperature_unit=celsius' | python3 -c "import json,sys; d=json.load(sys.stdin); cw=d.get('current_weather',{}); print(f\"{cw.get('weathercode', 'N/A')} {cw.get('temperature', 'N/A')}°C\")" 2>/dev/null || echo "N/A")

# Holiday definitions (date -> label)
declare -A HOLIDAYS=(
 ["2026-03-18"]="18 Mar: Nyepi (Bali Hindu New Year)"
 ["2026-03-19"]="19 Mar: Nyepi Day of Silence"
 ["2026-03-20"]="20 Mar: Lebaran Holiday"
 ["2026-03-21"]="21 Mar: Hari Raya Idul Fitri"
 ["2026-03-22"]="22 Mar: Hari Raya Idul Fitri"
 ["2026-04-03"]="03 Apr: Wafat Yesus Kristus (Good Friday)"
 ["2026-04-05"]="05 Apr: Hari Kebangkitan Yesus Kristus (Easter Sunday)"
 ["2026-05-01"]="01 May: Hari Buruh Nasional (Labour Day)"
 ["2026-05-14"]="14 May: Kenaikan Yesus Kristus (Ascension Day)"
 ["2026-05-15"]="15 May: Kenaikan Yesus Kristus"
 ["2026-05-27"]="27 May: Hari Raya Idul Adha 1447 Hijriah (Eid al-Adha)"
 ["2026-05-28"]="28 May: Idul Adha 1447 Hijriah"
)

# Find nearest holiday
NEAREST_HOLIDAY=""
NEAREST_DATE=""
for ((days=0; days<10; days++)); do
  check_date=$(date -u -d "+${days} days" '+%Y-%m-%d')
  if [[ -n "${HOLIDAYS[$check_date]:-}" ]]; then
    NEAREST_HOLIDAY="${HOLIDAYS[$check_date]}"
    NEAREST_DATE="$check_date"
    break
  fi
done
[[ -z "$NEAREST_HOLIDAY" ]] && NEAREST_HOLIDAY="No upcoming holidays in next 10 days"

# Find nearest cuti bersama that is NOT on the same day as the holiday
NEAREST_CUTI_BERSAMA=""
if [[ -n "$NEAREST_DATE" ]]; then
  for ((days=0; days<10; days++)); do
    check_date=$(date -u -d "+${days} days" '+%Y-%m-%d')
    if [[ -n "${HOLIDAYS[$check_date]:-}" && "$check_date" != "$NEAREST_DATE" ]]; then
      # Map date to cuti label (same as holiday label but with "Cuti bersama" prefix)
      case "$check_date" in
        "2026-03-18") NEAREST_CUTI_BERSAMA="18 Mar: Cuti bersama (Nyepi)" ;;
        "2026-03-19") NEAREST_CUTI_BERSAMA="19 Mar: Cuti bersama (Nyepi)" ;;
        "2026-03-20") NEAREST_CUTI_BERSAMA="20 Mar: Cuti bersama (Lebaran)" ;;
        "2026-03-21") NEAREST_CUTI_BERSAMA="21 Mar: Cuti bersama (Lebaran)" ;;
        "2026-03-22") NEAREST_CUTI_BERSAMA="22 Mar: Cuti bersama (Lebaran)" ;;
        "2026-04-03") NEAREST_CUTI_BERSAMA="03 Apr: Cuti bersama (Good Friday)" ;;
        "2026-04-05") NEAREST_CUTI_BERSAMA="05 Apr: Cuti bersama (Easter)" ;;
        "2026-05-01") NEAREST_CUTI_BERSAMA="01 May: Cuti bersama (Labour Day)" ;;
        "2026-05-14") NEAREST_CUTI_BERSAMA="14 May: Cuti bersama (Ascension)" ;;
        "2026-05-15") NEAREST_CUTI_BERSAMA="15 May: Cuti bersama (Ascension)" ;;
        "2026-05-27") NEAREST_CUTI_BERSAMA="27 May: Cuti bersama (Eid al-Adha)" ;;
        "2026-05-28") NEAREST_CUTI_BERSAMA="28 May: Cuti bersama (Eid al-Adha)" ;;
      esac
      break
    fi
  done
fi
[[ -z "$NEAREST_CUTI_BERSAMA" ]] && NEAREST_CUTI_BERSAMA="None in next 10 days"

# Build message with line breaks
TODAY=$(date -u +%Y-%m-%d)
RESEARCH_COUNT=$(find research -name "${TODAY}*.md" 2>/dev/null | wc -l)
CONTENT_COUNT=$(find content -name "${TODAY}*.md" 2>/dev/null | wc -l)
APPS_COUNT=$(grep -c "Generated app:" memory/code-gardener.log 2>/dev/null || echo 0)
SI_ACTIONS=0
SI_LOG=$(ls memory/self-improvement/${TODAY}T*.log 2>/dev/null | head -1)
if [ -n "$SI_LOG" ]; then
  SI_ACTIONS=$(grep -c "Applying (low-risk):" "$SI_LOG" 2>/dev/null || echo 0)
fi

MSG="Meta Summary (hourly):
Disk: ${DISK_PCT}%
Running agents: ${AGENTS}
Research reports today: ${REPORTS}
Content files today: ${CONTENT_COUNT}
Apps generated (24h): ${APPS_COUNT}
Self-improvements applied: ${SI_ACTIONS}
APT updates pending: ${UPDATES}
Weather (Bogor): ${WEATHER}
Next holiday: ${NEAREST_HOLIDAY}
Next cuti bersama: ${NEAREST_CUTI_BERSAMA}
All nominal. (◕‿◕)♡"

# Send to Telegram
openclaw message send --channel telegram --target 952170974 --message "$MSG" 2>/dev/null || echo "Failed to send summary: $MSG"
