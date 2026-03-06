#!/usr/bin/env bash
# Evolver Agent - Self-Improvement Cycle
# Runs the capability-evolver to analyze and improve the workspace

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOGFILE="$WORKSPACE/memory/evolver-agent.log"
SKILL_DIR="$WORKSPACE/skills/capability-evolver"

mkdir -p "$(dirname "$LOGFILE")"

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - Starting evolver-agent cycle" >> "$LOGFILE"

# Check if skill exists
if ! [ -f "$SKILL_DIR/index.js" ]; then
  echo "$(date -u) - ERROR: capability-evolver not found at $SKILL_DIR" >> "$LOGFILE"
  exit 1
fi

# Run evolver in autonomous balanced mode (repair + optimize + innovate)
# No --review: changes are applied after validation (surprise me!)
EVOLVE_STRATEGY=${EVOLVE_STRATEGY:-balanced}
AGENT_NAME=${AGENT_NAME:-main}

cd "$SKILL_DIR"
output=$(AGENT_NAME="$AGENT_NAME" EVOLVE_STRATEGY="$EVOLVE_STRATEGY" node index.js run 2>&1)
exit_code=$?

echo "$output" >> "$LOGFILE"

# Also append a summary to memory/evolver-summary.md for quick reference
SUMMARY_FILE="$WORKSPACE/memory/evolver-summary.md"
echo "## $(date -u '+%Y-%m-%d %H:%M:%S UTC') — evolver-agent cycle (exit $exit_code)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo '```' >> "$SUMMARY_FILE"
echo "$output" >> "$SUMMARY_FILE"
echo '```' >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

echo "$(date -u) - Evolver-agent cycle completed (exit $exit_code)" >> "$LOGFILE"
exit $exit_code
