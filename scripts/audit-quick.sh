#!/usr/bin/env bash
# Audit the quick launcher for common issues

WORKSPACE="/home/ubuntu/.openclaw/workspace"
QUICK="$WORKSPACE/quick"

echo "Quick Launcher Audit"
echo "--------------------"

if [ ! -f "$QUICK" ]; then
  echo "Error: quick file not found at $QUICK"
  exit 1
fi

# Check for duplicate command names
echo "Checking for duplicate case branches..."
dup=$(grep -E '^[[:space:]]*[a-zA-Z0-9_-]+\)' "$QUICK" | cut -d: -f1 | sort | uniq -d)
if [ -n "$dup" ]; then
  echo "⚠️  Duplicate command definitions found:"
  echo "$dup" | sed 's/^/  /'
else
  echo "✅ No duplicate command definitions"
fi

# Check for commands without matching function/script references
echo
echo "Checking case entries vs function definitions..."
case_commands=$(grep -E '^[[:space:]]*[a-zA-Z0-9_-]+\)' "$QUICK" | cut -d: -f1 | sort -u)
missing=0
for cmd in $case_commands; do
  # Look for the command in the case actions (the path to script)
  if grep -q "$cmd)" "$QUICK" && grep -A1 "$cmd)" "$QUICK" | grep -q '\$WORKSPACE/scripts/'; then
    # It exists; continue
    :
  else
    echo "⚠️  Command '$cmd' may not have a script mapping"
    missing=$((missing+1))
  fi
done
if [ $missing -eq 0 ]; then
  echo "✅ All case entries appear to have script mappings"
fi

# Check for consistent quoting and variable usage
echo
echo "Checking for common pitfalls..."
issues=0
if grep -q '\$@' "$QUICK"; then
  echo "  ℹ️  Uses \$@ (ensure proper quoting when passing arguments)"
fi
if grep -qE '\$[0-9]' "$QUICK"; then
  echo "  ℹ️  Uses positional parameters (may need validation)"
fi

# Count total commands
total=$(grep -c '^[[:space:]]*[a-zA-Z0-9_-]+\)' "$QUICK")
echo
echo "Audit complete: $total commands defined"
