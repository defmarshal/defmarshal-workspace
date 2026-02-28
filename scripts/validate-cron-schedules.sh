#!/usr/bin/env bash
# Validate and correct cron job schedules against CRON_JOBS.md documentation
# Now parses CRON_JOBS.md dynamically to avoid duplication and drift.

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/cron-schedules.log"
mkdir -p "$(dirname "$LOGFILE")" 2>/dev/null || true

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

# Ensure openclaw and jq are available
if ! command -v openclaw &>/dev/null; then
  log "ERROR: openclaw CLI not found"
  exit 1
fi
if ! command -v jq &>/dev/null; then
  log "ERROR: jq not installed (required for JSON parsing)"
  exit 1
fi

# Fetch cron jobs JSON, stripping any non-JSON preamble (Doctor warnings)
JSON=$(openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p')
if [ -z "$JSON" ]; then
  log "ERROR: Failed to fetch cron jobs JSON (empty after filtering)"
  exit 1
fi

# Validate JSON structure
if ! echo "$JSON" | jq empty 2>/dev/null; then
  log "ERROR: Cron list JSON is invalid. Dumping raw output for debugging:"
  openclaw cron list --json 2>/dev/null | head -20
  exit 1
fi

# Parse CRON_JOBS.md to extract job name, schedule, and timezone
# Format in docs: **job-name** followed by lines containing "Schedule: ... (`expr`)" and optional "Asia/Bangkok" or "UTC"
declare -A INTENDED_EXPR
declare -A INTENDED_TZ

while IFS= read -r line; do
  # Match bold job name: **job-name**
  if [[ "$line" =~ \*\*([^\*]+)\*\* ]]; then
    job="${BASH_REMATCH[1]}"
    # Read ahead to get schedule line and possibly tz line
    schedule_line=""
    tz=""
    read -r schedule_line
    if [[ "$schedule_line" =~ \`([^\`]+)\` ]]; then
      INTENDED_EXPR["$job"]="${BASH_REMATCH[1]}"
    fi
    read -r tz_line
    if [[ "$tz_line" =~ Asia/([A-Za-z_]+) ]]; then
      INTENDED_TZ["$job"]="Asia/${BASH_REMATCH[1]}"
    elif [[ "$tz_line" =~ UTC ]]; then
      INTENDED_TZ["$job"]="UTC"
    else
      INTENDED_TZ["$job"]="Asia/Bangkok"  # default
    fi
  fi
done < <(grep -n '^\s*[0-9]*\.\s*\*\*' /home/ubuntu/.openclaw/workspace/CRON_JOBS.md | cut -d: -f2-)

MISMATCHES=0
CORRECTED=0

for job in "${!INTENDED_EXPR[@]}"; do
  intended_expr="${INTENDED_EXPR[$job]}"
  intended_tz="${INTENDED_TZ[$job]:-Asia/Bangkok}"

  # Extract job info from JSON
  job_id=$(echo "$JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .id" 2>/dev/null || true)
  current_expr=$(echo "$JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .schedule.expr" 2>/dev/null || true)
  current_tz=$(echo "$JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .schedule.tz // empty" 2>/dev/null || true)

  if [ -z "$job_id" ]; then
    log "WARN: Job '$job' not found in cron list (maybe not created yet)"
    continue
  fi

  # Compare expr and tz
  if [ "$current_expr" != "$intended_expr" ] || [ "$current_tz" != "$intended_tz" ]; then
    log "MISMATCH: $job"
    log "  Current:  expr='$current_expr' tz='${current_tz:-<none>}'"
    log "  Intended: expr='$intended_expr' tz='$intended_tz'"

    # Update schedule
    if openclaw cron edit "$job_id" --cron "$intended_expr" --tz "$intended_tz" >>"$LOGFILE" 2>&1; then
      log "  Updated: $job -> $intended_expr @ $intended_tz"
      CORRECTED=$((CORRECTED+1))
    else
      log "  ERROR: Failed to update $job"
    fi
    MISMATCHES=$((MISMATCHES+1))
  fi
done

if [ $MISMATCHES -eq 0 ]; then
  log "All cron schedules match CRON_JOBS.md documentation."
else
  log "Cron schedule validation: $MISMATCHES mismatches detected, $CORRECTED corrected."
fi

exit 0
