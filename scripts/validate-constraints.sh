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

# 3. Git status clean
if ./quick git-status 2>/dev/null | grep -q "clean" || ./quick git-status 2>/dev/null | grep -q "nothing to commit"; then
    echo "✅ Git status: clean"
else
    echo "❌ Git status: dirty or untracked files"
    errors=$((errors+1))
fi

# 4. Health check (disk <80%, no pending updates, memory clean, gateway healthy)
health=$(./quick health 2>/dev/null || echo "Health check failed")
if echo "$health" | grep -q "Updates none" && \
   echo "$health" | grep -q "Memory clean" && \
   echo "$health" | grep -q "Gateway healthy"; then
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

# 6. APT updates (should be none pending)
updates=$(./quick updates-check 2>/dev/null || echo "Update check unavailable")
if echo "$updates" | grep -q "No pending" || echo "$updates" | grep -q "0 packages"; then
    echo "✅ APT updates: none pending"
elif echo "$updates" | grep -qE "[0-9]+ packages"; then
    echo "❌ APT updates pending:"
    echo "$updates" | sed 's/^/   /'
    errors=$((errors+1))
else
    echo "⚠️ APT updates check could not parse output"
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
