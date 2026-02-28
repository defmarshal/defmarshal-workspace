#!/usr/bin/env bash
set -euo pipefail

# Validate workspace constraints
# Exit 0 if all pass, 1 if any fail

cd "$(dirname "$0")/.."

errors=0

echo "Validating workspace constraints..."
echo ""

# 1. active-tasks.md size (≤2KB)
if [ -f "active-tasks.md" ]; then
    size=$(wc -c < active-tasks.md)
    if [ "$size" -le 2048 ]; then
        echo "✅ active-tasks.md size: $size bytes (≤2KB)"
    else
        echo "❌ active-tasks.md size: $size bytes (>2KB limit)"
        errors=$((errors+1))
    fi
else
    echo "❌ active-tasks.md not found"
    errors=$((errors+1))
fi

# 2. MEMORY.md line count (≤35 lines, buffer from 30)
if [ -f "MEMORY.md" ]; then
    lines=$(wc -l < MEMORY.md)
    if [ "$lines" -le 35 ]; then
        echo "✅ MEMORY.md lines: $lines (≤35)"
    else
        echo "❌ MEMORY.md lines: $lines (>35 limit)"
        errors=$((errors+1))
    fi
else
    echo "❌ MEMORY.md not found"
    errors=$((errors+1))
fi

# 3. Git status clean (git status --short should output nothing when clean)
if ./quick git-status 2>/dev/null | grep -q .; then
    echo "❌ Git status: dirty or untracked files"
    errors=$((errors+1))
else
    echo "✅ Git status: clean"
fi

# 4. Health check (disk <80%, no pending updates, memory clean, gateway healthy)
health=$(./quick health 2>/dev/null || echo "Health check failed")
if echo "$health" | grep -q "Updates.*none" && \
   echo "$health" | grep -q "clean" && \
   echo "$health" | grep -q "Gateway.*healthy"; then
    echo "✅ Health check: green"
else
    echo "❌ Health check: issues detected"
    echo "$health" | sed 's/^/   /'
    errors=$((errors+1))
fi

# 5. Temp files in workspace root
temp_files=$(find . -maxdepth 1 -type f \( -name "*.tmp" -o -name "*~" -o -name ".#*" -o -name "#*#" \) 2>/dev/null || true)
if [ -z "$temp_files" ]; then
    echo "✅ Temp files: none"
else
    echo "❌ Temp files detected:"
    echo "$temp_files" | sed 's/^/   /'
    errors=$((errors+1))
fi

# 5b. Shebang check for scripts/*.sh
sh_files=$(find scripts -type f -name "*.sh" 2>/dev/null || true)
missing_shebang=0
if [ -n "$sh_files" ]; then
    while IFS= read -r file; do
        first_line=$(head -n 1 "$file" 2>/dev/null || echo "")
        if ! echo "$first_line" | grep -q '^#!'; then
            echo "❌ Missing shebang in $file"
            missing_shebang=1
        fi
    done <<< "$sh_files"
fi
if [ $missing_shebang -ne 0 ]; then
    errors=$((errors+1))
elif [ -n "$sh_files" ]; then
    echo "✅ Shebang check: all scripts have #!"
else
    echo "⚠️ Shebang check: no .sh files found in scripts/"
fi

# 6. APT updates (should be none pending)
updates=$(./quick updates-check 2>/dev/null || echo "Update check unavailable")
if echo "$updates" | grep -q "All packages are up to date"; then
    echo "✅ APT updates: none pending"
elif echo "$updates" | grep -qE "[0-9]+ packages? can be upgraded"; then
    echo "❌ APT updates pending:"
    echo "$updates" | sed 's/^/   /'
    errors=$((errors+1))
else
    echo "⚠️ APT updates check could not parse output (non-critical)"
fi

# 7. Memory reindex age (warning if >3 days, error if >7 days)
REINDEX_LOG="memory/memory-reindex.log"
if [ -f "$REINDEX_LOG" ]; then
    AGE_DAYS=$(( ( $(date +%s) - $(stat -c %Y "$REINDEX_LOG") ) / 86400 ))
    if [ "$AGE_DAYS" -le 3 ]; then
        echo "✅ Memory reindex age: $AGE_DAYS day(s) (fresh)"
    elif [ "$AGE_DAYS" -le 7 ]; then
        echo "⚠️ Memory reindex age: $AGE_DAYS day(s) (stale, consider reindex)"
    else
        echo "❌ Memory reindex age: $AGE_DAYS day(s) (very stale, reindex needed)"
        errors=$((errors+1))
    fi
else
    echo "⚠️ Memory reindex log not found (cannot assess reindex age)"
fi

# 8. Branch hygiene: stale idea branches (informational)
STALE_THRESHOLD_DAYS=7
# Get local idea branches
stale_branches=$(git branch --list 'idea/*' 2>/dev/null | while read branch; do
    clean_branch=$(echo "$branch" | sed 's/^\*\s*//')
    last_commit_ts=$(git log -1 --format=%ct "$clean_branch" 2>/dev/null || echo 0)
    if [ "$last_commit_ts" -gt 0 ]; then
        age_days=$(( ( $(date +%s) - last_commit_ts ) / 86400 ))
        if [ "$age_days" -ge "$STALE_THRESHOLD_DAYS" ]; then
            echo "$clean_branch ($age_days days old)"
        fi
    fi
done)

if [ -n "$stale_branches" ]; then
    echo "⚠️ Stale idea branches (≥${STALE_THRESHOLD_DAYS} days):"
    echo "$stale_branches" | sed 's/^/   /'
else
    echo "✅ Branch hygiene: no stale idea branches"
fi

# Summary
echo ""
if [ "$errors" -eq 0 ]; then
    echo "✅ All constraints satisfied."
    exit 0
else
    echo "❌ Constraint violations detected: $errors check(s) failed."
    exit 1
fi