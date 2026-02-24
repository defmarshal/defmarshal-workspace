#!/usr/bin/env bash
# Validate timestamp arithmetic in agent scripts for octal parsing safety

WORKSPACE="/home/ubuntu/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE/agents"

echo "Timestamp Arithmetic Validation"
echo "--------------------------------"

find "$SCRIPTS_DIR" -type f -name "*.sh" | while read -r script; do
  echo "Checking: $script"
  # Look for date -u +%H or %M used in arithmetic expansion $((...))
  # Without 10# prefix, leading zeros cause octal errors
  ISSUES=$(grep -n -E '\$\(date -u \+%[HM]' "$script" | grep -v '10#')
  if [ -n "$ISSUES" ]; then
    echo "  ⚠️  Potential octal parsing:"
    echo "$ISSUES" | sed 's/^/    line /'
    echo "  Fix: use 10#\$HOUR or strip leading zeros (HOUR=\$(date -u +%H | sed 's/^0*//'))"
  else
    echo "  ✅ OK"
  fi
done

echo
echo "Done. Fix any reported lines to avoid 'value too great for base' errors."
