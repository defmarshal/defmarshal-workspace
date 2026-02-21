#!/usr/bin/env bash
# Rotate agent logs (compression and retention)

set -euo pipefail
WORKSPACE="${WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
LOGS_DIR="$WORKSPACE/logs"
RETENTION_DAYS="${RETENTION_DAYS:-30}"  # keep last 30 days
MAX_SIZE_MB="${MAX_SIZE_MB:-100}"        # rotate if > 100MB

mkdir -p "$LOGS_DIR"

rotate_if_large() {
  local logfile="$1"
  if [ ! -f "$logfile" ]; then
    return 0
  fi
  local size_mb=$(du -m "$logfile" | cut -f1)
  if [ "$size_mb" -ge "$MAX_SIZE_MB" ]; then
    local ts=$(date -u +%Y%m%d-%H%M%S)
    local rotated="${logfile}.${ts}.gz"
    gzip -c "$logfile" > "$rotated"
    echo > "$logfile"
    echo "Rotated $(basename "$logfile") -> $(basename "$rotated")"
  fi
}

# Rotate large active logs
for log in "$WORKSPACE"/*.log; do
  [ -e "$log" ] || continue
  rotate_if_large "$log"
done

# Delete old rotated logs (older than RETENTION_DAYS)
find "$LOGS_DIR" -name "*.log.*.gz" -type f -mtime +"$RETENTION_DAYS" -delete 2>/dev/null || true

# Rotate any logs still in memory/ (agent logs)
find "$WORKSPACE/memory" -name "*.log" -type f -exec bash -c '
  for f; do
    if [ -f "$f" ]; then
      size_mb=$(du -m "$f" | cut -f1)
      if [ "$size_mb" -ge 100 ]; then
        ts=$(date -u +%Y%m%d-%H%M%S)
        dest="${f}.${ts}.gz"
        gzip -c "$f" > "$dest"
        echo > "$f"
        echo "Rotated $(basename "$f") -> $(basename "$dest")"
      fi
    fi
  done
' bash {} +

echo "Log cleanup complete."
