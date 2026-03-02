#!/usr/bin/env bash
# Show idea pipeline health and status
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

echo "=== Idea Pipeline Health ==="
echo ""

# Check status.json
if [ -f "agents/ideas/status.json" ]; then
    status=$(jq -r '.status // "unknown"' agents/ideas/status.json 2>/dev/null || echo "error")
    last_run=$(jq -r '.last_run // "never"' agents/ideas/status.json 2>/dev/null || echo "unknown")
    echo "Executor status:  $status"
    echo "Last executor run: $last_run"
else
    echo "Executor status:  no status file found"
    echo "Last executor run: unknown"
fi

# Check generator last run via log
echo ""
echo "Generator activity:"
if [ -f "memory/idea-generator.log" ]; then
    gen_last=$(tail -1 memory/idea-generator.log 2>/dev/null | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}' || echo "no entries")
    echo "Last generator log: $gen_last"
else
    echo "Last generator log: no log file"
fi

# Pending ideas count
if [ -f "agents/ideas/latest.json" ]; then
    pending_count=$(jq 'length' agents/ideas/latest.json 2>/dev/null || echo "0")
    echo "Pending ideas:    $pending_count"
else
    echo "Pending ideas:    no ideas file"
fi

# Recent executor errors (last 20 lines, filter ERROR)
echo ""
echo "Recent executor activity (last 5 ERROR/FAIL lines, if any):"
if [ -f "memory/idea-executor.log" ]; then
    error_count=$(tail -100 memory/idea-executor.log 2>/dev/null | grep -ciE 'ERROR|VALIDATION FAILED|Rejected' || echo "0")
    if [ "$error_count" -gt 0 ]; then
        tail -100 memory/idea-executor.log 2>/dev/null | grep -iE 'ERROR|VALIDATION FAILED|Rejected' | tail -5 | sed 's/^/  /'
    else
        echo "  (no recent errors detected)"
    fi
else
    echo "  (no executor log)"
fi

echo ""
echo "=== End of report ==="
