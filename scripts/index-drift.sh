#!/usr/bin/env bash
# Check for drift between actual files and INDEX.md entries
# Detects missing INDEX entries for research/ and content/ directories
# Usage: quick index-drift [--fix]

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
FIX=0
[[ "${1:-}" == "--fix" ]] && FIX=1

ISSUES=0

# Files to exclude from drift checks (planning artifacts, non-reports)
RESEARCH_EXCLUDES="INDEX findings task_plan test-report progress watchlist cycle-summary"

check_dir() {
  local dir="$1"
  local excludes="$2"
  local index="$WORKSPACE/$dir/INDEX.md"

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  📂 $dir/INDEX.md drift check"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [[ ! -f "$index" ]]; then
    echo "  ⚠️  No INDEX.md found in $dir/"
    return
  fi

  local missing=0
  while IFS= read -r f; do
    base=$(basename "$f")
    # Skip files without date prefix (planning artifacts: findings.md, task_plan.md, etc.)
    [[ ! "$base" =~ ^[0-9]{4}-[0-9]{2} ]] && continue
    # Skip excluded patterns
    skip=0
    for excl in $excludes; do
      [[ "$base" == *"$excl"* ]] && skip=1 && break
    done
    [[ $skip -eq 1 ]] && continue

    if ! grep -q "$base" "$index" 2>/dev/null; then
      echo "  ❌ MISSING from INDEX: $base"
      missing=$((missing + 1))
      ISSUES=$((ISSUES + 1))
    fi
  done < <(find "$WORKSPACE/$dir" -maxdepth 1 -name "*.md" -type f | sort)

  if [[ $missing -eq 0 ]]; then
    total=$(find "$WORKSPACE/$dir" -maxdepth 1 -name "*.md" -type f \
      | grep -E "/[0-9]{4}-[0-9]{2}" | wc -l)
    echo "  ✅ All $total date-prefixed files accounted for in INDEX"
  else
    echo "  ⚠️  $missing files missing from INDEX"
    [[ $FIX -eq 1 ]] && echo "  🔧 --fix: run 'quick content-index-update' for content; research INDEX is manually maintained"
  fi
  echo ""
}

check_dir "research" "$RESEARCH_EXCLUDES"
check_dir "content" "INDEX"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $ISSUES -eq 0 ]]; then
  echo "  ✅ No drift detected — all date-prefixed files tracked in INDEX"
else
  echo "  ⚠️  Total drift: $ISSUES files missing from INDEX"
  echo "  Tip: run 'quick content-index-update' to regenerate content INDEX"
fi
echo ""
