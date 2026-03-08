#!/bin/bash
# qwen-wrapper — logs usage and forwards to qwen CLI
set -u

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory/qwen-monitor"
LOG_FILE="$LOG_DIR/qwen-usage.log"
mkdir -p "$LOG_DIR"

# Parse arguments
APPROVAL_MODE="default"
if [[ " $* " =~ " --approval-mode " ]]; then
  APPROVAL_MODE=$(echo "$@" | sed -n 's/.*--approval-mode \([a-z]*\).*/\1/p')
fi
MODEL=""
if [[ " $* " =~ " -m " ]] || [[ " $* " =~ " --model " ]]; then
  MODEL=$(echo "$@" | sed -n 's/.*\(-m\|--model\) \([a-zA-Z0-9-]*\).*/\2/p')
fi

# Log entry
echo "[$(date -u '+%Y-%m-%d %H:%M:%S') UTC] qwen $* | model=$MODEL approval=$APPROVAL_MODE" >> "$LOG_FILE"

# Execute qwen
exec qwen "$@"
