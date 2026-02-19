#!/usr/bin/env bash
# Validate and correct cron job schedules against CRON_JOBS.md documentation
# Uses openclaw cron list --json for reliable parsing.

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

LOGFILE="memory/cron-schedules.log"
mkdir -p "$(dirname "$LOGFILE")" 2>/dev/null || true

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}
# tz defaults to Asia/Bangkok if not specified, but we store both.
declare -A INTENDED_EXPR=(
  ["workspace-builder"]="0 */2 * * *"
  ["vishwakarma-cron"]="0 */4 * * *"
  ["agent-manager-cron"]="0,30 * * * *"
  ["supervisor-cron"]="0,30 * * * *"
  ["meta-agent-cron"]="0 * * * *"
  ["random-torrent-downloader"]="0 */2 * * *"
  ["agni-cron"]="0 */2 * * *"
  ["auto-torrent-cron"]="0 2 * * *"
  ["content-index-update-cron"]="30 5 * * *"
  ["dev-agent-cron"]="0 8-22 * * *"
  ["content-agent-cron"]="0 8-22 * * *"
  ["research-agent-cron"]="0 8-22 * * *"
  ["daily-digest-cron"]="0 12,20 * * *"
  ["memory-reindex-cron"]="0 4 * * 0"
  ["log-rotate-cron"]="0 5 * * 0"
  ["cleanup-downloads-cron"]="0 6 * * 0"
  ["backup-cleanup-cron"]="0 7 * * 0"
  ["cleanup-agent-artifacts-cron"]="30 9 * * 0"
)

declare -A INTENDED_TZ=(
  ["workspace-builder"]="Asia/Bangkok"
  ["vishwakarma-cron"]="Asia/Bangkok"
  ["agent-manager-cron"]="Asia/Bangkok"
  ["supervisor-cron"]="Asia/Bangkok"
  ["meta-agent-cron"]="Asia/Bangkok"
  ["random-torrent-downloader"]="UTC"
  ["agni-cron"]="UTC"
  ["auto-torrent-cron"]="Asia/Bangkok"
  ["content-index-update-cron"]="Asia/Bangkok"
  ["dev-agent-cron"]="Asia/Bangkok"
  ["content-agent-cron"]="Asia/Bangkok"
  ["research-agent-cron"]="Asia/Bangkok"
  ["daily-digest-cron"]="Asia/Bangkok"
  ["memory-reindex-cron"]="Asia/Bangkok"
  ["log-rotate-cron"]="Asia/Bangkok"
  ["cleanup-downloads-cron"]="Asia/Bangkok"
  ["backup-cleanup-cron"]="Asia/Bangkok"
  ["cleanup-agent-artifacts-cron"]="Asia/Bangkok"
)

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*"
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

# Fetch cron jobs JSON
CRON_JSON=$(openclaw cron list --json 2>/dev/null)
if [ -z "$CRON_JSON" ]; then
  log "ERROR: Failed to fetch cron jobs JSON"
  exit 1
fi

MISMATCHES=0
CORRECTED=0

for job in "${!INTENDED_EXPR[@]}"; do
  intended_expr="${INTENDED_EXPR[$job]}"
  intended_tz="${INTENDED_TZ[$job]:-Asia/Bangkok}"  # default to Asia/Bangkok if not set

  # Extract job info from JSON
  job_id=$(echo "$CRON_JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .id" 2>/dev/null || true)
  current_expr=$(echo "$CRON_JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .schedule.expr" 2>/dev/null || true)
  current_tz=$(echo "$CRON_JSON" | jq -r ".jobs[] | select(.name==\"$job\") | .schedule.tz // empty" 2>/dev/null || true)

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
