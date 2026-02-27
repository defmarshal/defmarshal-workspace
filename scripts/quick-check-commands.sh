#!/usr/bin/env bash
# quick check-commands — sanity check core quick commands (dry-run where possible)
# Exits non-zero if any command fails.

set -euo pipefail
WORKSPACE="${WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
cd "$WORKSPACE"

FAILED=0

# health snapshot (safe, read-only)
if ! ./quick health-snapshot >/dev/null 2>&1; then
  echo "❌ health-snapshot failed"
  FAILED=1
fi

# validate-constraints (safe)
if ! ./quick validate-constraints >/dev/null 2>&1; then
  echo "❌ validate-constraints failed"
  FAILED=1
fi

# list agents (safe)
if ! ./quick agents >/dev/null 2>&1; then
  echo "❌ agents failed"
  FAILED=1
fi

# git-status (safe)
if ! ./quick git-status >/dev/null 2>&1; then
  echo "❌ git-status failed"
  FAILED=1
fi

# memory-status (safe)
if ! ./quick memory-status >/dev/null 2>&1; then
  echo "❌ memory-status failed"
  FAILED=1
fi

# time (safe)
if ! ./quick time >/dev/null 2>&1; then
  echo "❌ time failed"
  FAILED=1
fi

# agent-status (safe)
if ! ./quick agent-status >/dev/null 2>&1; then
  echo "❌ agent-status failed"
  FAILED=1
fi

if [ $FAILED -eq 0 ]; then
  echo "✅ All checked quick commands OK"
else
  echo "Some commands failed. Review output above."
fi
exit $FAILED
