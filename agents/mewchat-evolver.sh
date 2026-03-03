#!/usr/bin/env bash
# MewChat Evolver — continuous improvement agent
# Runs every 6 hours via cron

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/memory"
LOG_FILE="$LOG_DIR/mewchat-evolver.log"
MEWCHAT_DIR="$WORKSPACE/apps/mewchat"

echo "=== MewChat Evolver started at $(TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M') ===" | tee -a "$LOG_FILE"

# Change to mewchat dir
cd "$MEWCHAT_DIR"

# 1) List current files (for context)
echo "Current files:" | tee -a "$LOG_FILE"
ls -la | tee -a "$LOG_FILE"

# 2) Propose an improvement (using openclaw agent)
# We'll ask the main agent to perform a specific improvement task
IMPROVEMENT_PROMPT="You are the MewChat evolution agent. Examine the MewChat codebase and implement ONE small improvement. Focus on:
- UX/UI polish (animations, responsiveness)
- Performance (asset size, caching)
- Features (PWA, themes, notifications)
- Code quality (error handling, readability)
- Accessibility

Current files are in /home/ubuntu/.openclaw/workspace/apps/mewchat/. Implement a concrete change, test it quickly with a local server if needed, then commit with a clear message. Keep changes minimal and focused.

Reply ONLY with a summary of what you changed."
echo "Sending improvement prompt to main agent..." | tee -a "$LOG_FILE"

# Run the agent turn (non-interactive)
openclaw agent --agent main --message "$IMPROVEMENT_PROMPT" --thinking low --timeout 600 2>&1 | tee -a "$LOG_FILE"

echo "=== Evolver cycle completed ===" | tee -a "$LOG_FILE"