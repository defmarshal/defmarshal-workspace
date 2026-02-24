#!/usr/bin/env bash
# Workspace Hygiene Checker
# Scans for common issues: CRLF line endings, missing exec permissions, large untracked files
# Safe: read-only; does not modify anything

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

echo "== Workspace Hygiene Check =="
echo ""

# 1. Check for CRLF line endings in tracked files
echo "1. Tracking CRLF line endings in tracked files..."
CRLF_COUNT=0
while IFS= read -r file; do
  # Use grep -I to ignore binary files (avoid false positives)
  if grep -qI $'\r' "$file" 2>/dev/null; then
    echo "   ⚠ CRLF found: $file"
    ((CRLF_COUNT++))
  fi
done < <(git ls-files)
if [ "$CRLF_COUNT" -eq 0 ]; then
  echo "   ✓ No CRLF in tracked files"
fi

# 2. Check for common scripts missing executable bit
echo ""
echo "2. Checking common script directories for missing exec bits..."
MISSING_EXEC=0
while IFS= read -r script; do
  if [ ! -x "$script" ]; then
    echo "   ⚠ Not executable: $script"
    ((MISSING_EXEC++))
  fi
done < <(find . -type f \( -name "*.sh" -o -name "quick" \) -not -path "*/\.git/*")
if [ "$MISSING_EXEC" -eq 0 ]; then
  echo "   ✓ All shell scripts appear executable"
fi

# 3. Check for large untracked files (potential disk hogs)
echo ""
echo "3. Scanning for large untracked files (>100 MB)..."
LARGE_FILES=0
while IFS= read -r file; do
  size_mb=$(du -m "$file" | cut -f1)
  if [ "$size_mb" -ge 100 ]; then
    echo "   ⚠ $file (${size_mb} MB)"
    ((LARGE_FILES++))
  fi
done < <(git status --porcelain | grep '^??' | awk '{print $2}')
if [ "$LARGE_FILES" -eq 0 ]; then
  echo "   ✓ No large untracked files (>100 MB)"
fi

# 4. Check for __pycache__ directories not ignored
echo ""
echo "4. Checking for __pycache__ directories (should be ignored)..."
PYCACHE_DIRS=$(find . -type d -name "__pycache__" | head -5)
if [ -n "$PYCACHE_DIRS" ]; then
  echo "   ⚠ Found __pycache__ directories (these should be ignored by git)"
  echo "$PYCACHE_DIRS"
else
  echo "   ✓ No __pycache__ directories found"
fi

# 5. Quick summary
echo ""
echo "== Summary =="
echo "CRLF issues: $CRLF_COUNT lines"
echo "Missing exec bits: $MISSING_EXEC scripts"
echo "Large untracked files: $LARGE_FILES"
echo ""
echo "Note: This is a read-only check. No changes were made."