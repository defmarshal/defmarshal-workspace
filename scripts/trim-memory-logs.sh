#!/usr/bin/env bash
# trim-memory-logs.sh — trim oversized memory/*.log files to a line-count threshold
# Usage: scripts/trim-memory-logs.sh [--threshold N] [--execute]
# Default: dry-run, threshold 1000 lines
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

THRESHOLD=1000
DRY_RUN=true

for arg in "$@"; do
  case "$arg" in
    --threshold) shift; THRESHOLD="${1:-1000}" ;;
    --threshold=*) THRESHOLD="${arg#*=}" ;;
    --execute) DRY_RUN=false ;;
  esac
done

echo "== Memory Log Trim $(date -u -Iseconds) =="
echo "Threshold: ${THRESHOLD} lines | Mode: $([ "$DRY_RUN" = true ] && echo 'dry-run' || echo 'execute')"
echo ""

TRIMMED=0
for logfile in memory/*.log; do
  [[ -f "$logfile" ]] || continue
  lines=$(wc -l < "$logfile")
  if (( lines > THRESHOLD )); then
    excess=$(( lines - THRESHOLD ))
    size_before=$(du -h "$logfile" | cut -f1)
    if [ "$DRY_RUN" = true ]; then
      echo "  [DRY] $logfile: $lines lines ($size_before) → would trim $excess lines"
    else
      tail -"${THRESHOLD}" "$logfile" > "${logfile}.tmp" && mv "${logfile}.tmp" "$logfile"
      size_after=$(du -h "$logfile" | cut -f1)
      echo "  [OK] $logfile: trimmed $excess lines ($size_before → $size_after)"
      TRIMMED=$(( TRIMMED + 1 ))
    fi
  fi
done

if [ "$DRY_RUN" = false ]; then
  echo ""
  echo "Trimmed $TRIMMED log(s)."
else
  echo ""
  echo "Dry-run complete. Pass --execute to apply."
fi
