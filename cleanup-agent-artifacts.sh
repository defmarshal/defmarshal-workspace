#!/usr/bin/env bash
# Cleanup stale agent artifacts (lock files, empty plan files)
# Safe by default: shows what would be deleted; use --execute to actually delete
# Respects quiet hours (skips execution during 23:00-08:00 Asia/Bangkok unless forced)

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

DRY_RUN=true
FORCE=false

usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Clean up stale agent artifacts:
- Stale lock files (>1 hour old) in agent directories
- Empty or near‑empty plan files (< 10 bytes)

Options:
  --execute    Actually delete files (default: dry-run only)
  --force      (Deprecated) Kept for compatibility; no longer needed
  -h, --help   Show this help message

Examples:
  $0                       # Dry-run: show what would be deleted
  $0 --execute             # Delete stale artifacts (runs 24/7)
EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --execute)
      DRY_RUN=false
      shift
      ;;
    --force)
      # Kept for backward compatibility; no longer needed but harmless
      FORCE=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

# Note: Quiet hours were removed system-wide on 2026-02-17; all agents run 24/7.
# The --force flag is retained for compatibility but has no effect.

echo "== Agent Artifact Cleanup =="
echo "Workspace: $WORKSPACE"
echo "Mode: $([ "$DRY_RUN" = true ] && echo 'DRY-RUN (no changes)' || echo 'EXECUTE')"
echo ""

# 1. Stale lock files
echo "Scanning for stale lock files (>1 hour old)..."
found_locks=0
while IFS= read -r lockfile; do
  age_sec=$(( $(date +%s) - $(stat -c %Y "$lockfile") ))
  if [ $age_sec -gt 3600 ]; then
    found_locks=$((found_locks+1))
    age_h=$(( age_sec / 3600 ))
    if [ "$DRY_RUN" = true ]; then
      echo "  Would delete: $lockfile (stale, age: ${age_h}h)"
    else
      echo "  Deleting: $lockfile (stale, age: ${age_h}h)"
      rm -f "$lockfile"
    fi
  fi
done < <(find . -name ".lock" -type f 2>/dev/null)

if [ $found_locks -eq 0 ]; then
  echo "  No stale locks found."
fi

# 2. Empty/near-empty plan files
echo ""
echo "Scanning for empty or near‑empty plan files (< 10 bytes)..."
found_plans=0
while IFS= read -r planfile; do
  size=$(stat -c %s "$planfile")
  if [ $size -lt 10 ]; then
    found_plans=$((found_plans+1))
    if [ "$DRY_RUN" = true ]; then
      echo "  Would delete: $planfile (size: ${size}B)"
    else
      echo "  Deleting: $planfile (size: ${size}B)"
      rm -f "$planfile"
    fi
  fi
done < <(find agents -path "*/plans/*.md" -type f 2>/dev/null)

if [ $found_plans -eq 0 ]; then
  echo "  No empty plan files found."
fi

echo ""
echo "Cleanup complete."
if [ "$DRY_RUN" = true ]; then
  echo "Add --execute to perform deletion."
fi