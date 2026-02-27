#!/usr/bin/env bash
# enhancement-bot-daemon.sh — automatically processes enhancement proposals
# PID: memory/enhancement-bot.pid ; Log: memory/enhancement-bot.log

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

PID_FILE="$WORKSPACE/memory/enhancement-bot.pid"
LOG_FILE="$WORKSPACE/memory/enhancement-bot.log"

# Single instance guard
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Enhancement bot already running (PID $(cat "$PID_FILE"))."
  exit 0
fi
echo $$ > "$PID_FILE"
trap 'rm -f "$PID_FILE"; exit' INT TERM EXIT

log() {
  echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - $*" | tee -a "$LOG_FILE"
}

log "Enhancement bot daemon started"

while true; do
  # Find best ready/proposed item (lowest priority number = highest priority)
  ITEM=$(find enhancements -name '*.json' 2>/dev/null | while read -r f; do
    STATUS=$(jq -r '.status' "$f" 2>/dev/null || echo "unknown")
    if [[ "$STATUS" == "ready" || "$STATUS" == "proposed" ]]; then
      PRIORITY=$(jq -r '.priority // 5' "$f" 2>/dev/null || echo 5)
      MTIME=$(stat -c %Y "$f")
      printf "%02d %d %s\n" "$PRIORITY" "$MTIME" "$f"
    fi
  done | sort -n -k1,1 -k2,2 | head -1 | cut -d' ' -f3-)

  if [ -z "$ITEM" ]; then
    sleep 30
    continue
  fi

  log "Processing: $ITEM"
  SCRIPT=$(jq -r '.script' "$ITEM" 2>/dev/null || echo "")
  if [ -z "$SCRIPT" ] || [ ! -x "$SCRIPT" ]; then
    log "ERROR: Missing or non-executable script: $SCRIPT"
    jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.status="failed", failed_at=$ts, result="Script missing or not executable"' "$ITEM" > "$ITEM.tmp" && mv "$ITEM.tmp" "$ITEM"
    sleep 2
    continue
  fi

  OUTPUT=$(mktemp)
  set +e
  "$SCRIPT" > "$OUTPUT" 2>&1
  EXIT_CODE=$?
  set -e

  if [ $EXIT_CODE -eq 0 ]; then
    log "SUCCESS: $ITEM"
    if jq --arg status "implemented" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg result "$(cat "$OUTPUT")" \
      '.status = $status, .implemented_at = $ts, .result = $result' "$ITEM" > "$ITEM.tmp"; then
      if mv "$ITEM.tmp" "$ITEM"; then
        log "Updated proposal status to implemented"
      else
        log "ERROR: mv failed for $ITEM.tmp -> $ITEM"
        rm -f "$ITEM.tmp"
      fi
    else
      log "ERROR: jq failed for $ITEM"
      rm -f "$ITEM.tmp"
    fi
  else
    log "FAILED: $ITEM (exit $EXIT_CODE). Output: $(cat "$OUTPUT")"
    if jq --arg status "failed" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg result "$(cat "$OUTPUT")" \
      '.status = $status, .failed_at = $ts, .result = $result' "$ITEM" > "$ITEM.tmp"; then
      if mv "$ITEM.tmp" "$ITEM"; then
        log "Updated proposal status to failed"
      else
        log "ERROR: mv failed for $ITEM.tmp -> $ITEM"
        rm -f "$ITEM.tmp"
      fi
    else
      log "ERROR: jq failed for $ITEM"
      rm -f "$ITEM.tmp"
    fi
  fi
  rm -f "$OUTPUT"

  sleep 10
done
