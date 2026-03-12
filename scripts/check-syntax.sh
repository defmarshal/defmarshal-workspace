#!/usr/bin/env bash
# Workspace-wide Python syntax checker
# Usage: ./scripts/check-syntax.sh [pattern]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
PATTERN="${1:-*.py}"

echo "🔍 Checking Python syntax in workspace..."
echo "Pattern: $PATTERN"
echo ""

errors=0
while IFS= read -r -d '' file; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "✓ $file"
    else
        echo "✗ $file — SYNTAX ERROR"
        ((errors++))
    fi
done < <(find "$WORKSPACE" -name "$PATTERN" ! -path "./valhalla-jabodetabek/*" ! -path "./.git/*" -print0)

echo ""
if [ $errors -eq 0 ]; then
    echo "✅ All Python files compile successfully."
    exit 0
else
    echo "❌ Found $errors file(s) with syntax errors."
    exit 1
fi
