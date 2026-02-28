#!/usr/bin/env bash
# trim-agent-logs.sh — Trim oversized agent log files in memory/
# Keeps the last N lines of any .log file exceeding SIZE_THRESHOLD bytes.
# Appends a trim marker so history isn't silently lost.
#
# Usage:
#   scripts/trim-agent-logs.sh [--size KB] [--keep LINES] [--dry-run] [--dir DIR]
#
# Defaults:
#   --size   500   (KB) — trim logs larger than this
#   --keep  1000   (lines) — keep the last N lines after trimming
#   --dir    memory/

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

# Defaults
SIZE_THRESHOLD_KB=500
KEEP_LINES=1000
DRY_RUN=false
LOG_DIR="memory"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --size)   SIZE_THRESHOLD_KB="$2"; shift 2 ;;
    --keep)   KEEP_LINES="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --dir)    LOG_DIR="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--size KB] [--keep LINES] [--dry-run] [--dir DIR]"
      exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

SIZE_THRESHOLD_BYTES=$(( SIZE_THRESHOLD_KB * 1024 ))
TRIMMED=0
SKIPPED=0

echo "== Agent Log Trim — $(date -u +%Y-%m-%dT%H:%M:%SZ) =="
echo "Threshold: ${SIZE_THRESHOLD_KB}KB | Keep: ${KEEP_LINES} lines | Dir: ${LOG_DIR}/ | Dry-run: ${DRY_RUN}"
echo ""

while IFS= read -r -d '' logfile; do
  size=$(stat -c%s "$logfile" 2>/dev/null || echo 0)
  if (( size <= SIZE_THRESHOLD_BYTES )); then
    SKIPPED=$(( SKIPPED + 1 ))
    continue
  fi

  size_kb=$(( size / 1024 ))
  lines=$(wc -l < "$logfile")
  echo "  Trimming: $logfile (${size_kb}KB, ${lines} lines → keep last ${KEEP_LINES})"

  if [[ "$DRY_RUN" == "true" ]]; then
    TRIMMED=$(( TRIMMED + 1 ))
    continue
  fi

  # Trim: keep last KEEP_LINES lines, prepend a marker
  tmp="${logfile}.trim.tmp"
  {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [trim-agent-logs] === Log trimmed: kept last ${KEEP_LINES} of ${lines} lines (was ${size_kb}KB) ==="
    tail -n "$KEEP_LINES" "$logfile"
  } > "$tmp"
  mv "$tmp" "$logfile"

  new_size=$(stat -c%s "$logfile" 2>/dev/null || echo 0)
  new_kb=$(( new_size / 1024 ))
  echo "    → Trimmed to ${new_kb}KB"
  TRIMMED=$(( TRIMMED + 1 ))
done < <(find "$LOG_DIR" -maxdepth 1 -name "*.log" -print0 2>/dev/null)

echo ""
echo "Done. Trimmed: ${TRIMMED} | Skipped (under threshold): ${SKIPPED}"
