#!/usr/bin/env bash
# disk-usage-breakdown.sh — Workspace disk usage by top-level directory
# Shows sizes, flags large dirs, and identifies growth areas.
#
# Usage: scripts/disk-usage-breakdown.sh [--top N] [--threshold MB] [--json]

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
TOP=20
THRESHOLD_MB=100
JSON=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --top)      TOP="$2"; shift 2 ;;
    --threshold) THRESHOLD_MB="$2"; shift 2 ;;
    --json)     JSON=true; shift ;;
    -h|--help)
      echo "Usage: $0 [--top N] [--threshold MB] [--json]"
      echo "  --top N         Show top N entries (default: 20)"
      echo "  --threshold MB  Flag dirs above this size in MB (default: 100)"
      echo "  --json          Output JSON array"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

cd "$WORKSPACE"

# Gather sizes
mapfile -t entries < <(du -sm */ .[!.]* 2>/dev/null | sort -rn | head -"$TOP")

if [[ "$JSON" == "true" ]]; then
  echo "["
  first=true
  for entry in "${entries[@]}"; do
    size_mb=$(echo "$entry" | awk '{print $1}')
    dir=$(echo "$entry" | awk '{print $2}')
    flag=""
    if (( size_mb >= THRESHOLD_MB )); then flag="large"; fi
    if [[ "$first" == "true" ]]; then first=false; else echo ","; fi
    printf '  {"dir":"%s","size_mb":%s,"flag":"%s"}' "$dir" "$size_mb" "$flag"
  done
  echo ""
  echo "]"
  exit 0
fi

# Human-readable output
echo "╔══════════════════════════════════════════════════╗"
echo "║   Workspace Disk Usage — $(date -u '+%Y-%m-%d %H:%M UTC')    ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Total workspace
total_mb=$(du -sm "$WORKSPACE" 2>/dev/null | awk '{print $1}')
disk_info=$(df -h "$WORKSPACE" | tail -1 | awk '{print $3"/"$2, "("$5" used)"}')
echo "  Workspace total : ${total_mb}MB"
echo "  Disk used       : $disk_info"
echo ""

printf "%-32s %8s  %s\n" "DIRECTORY" "SIZE" "STATUS"
echo "$(printf '─%.0s' {1..55})"

for entry in "${entries[@]}"; do
  size_mb=$(echo "$entry" | awk '{print $1}')
  dir=$(echo "$entry" | awk '{print $2}')

  # Format size
  if (( size_mb >= 1024 )); then
    size_fmt="$(echo "scale=1; $size_mb/1024" | bc)GB"
  else
    size_fmt="${size_mb}MB"
  fi

  # Flag
  if (( size_mb >= 1024 )); then
    status="🔴 large"
  elif (( size_mb >= THRESHOLD_MB )); then
    status="🟡 monitor"
  else
    status="✅ ok"
  fi

  printf "%-32s %8s  %s\n" "${dir:0:32}" "$size_fmt" "$status"
done

echo ""
echo "Tip: Use 'quick find-large-files --dir <dir>' to drill down."
