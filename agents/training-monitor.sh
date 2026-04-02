#!/usr/bin/env bash
# Monitor TinyLlama training process and log activity
# Sends Telegram alerts on errors, crashes, or staleness

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
LOG_FILE="$WORKSPACE/memory/tinyllama-training-retry.log"
STATE_FILE="$WORKSPACE/memory/training-monitor-state.json"
ALERT_COOLDOWN=1800  # 30 minutes between repeat alerts

# Timestamp function
timestamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }

# Log to console
log() { echo "[$(timestamp)] $*"; }

# Load state
if [ -f "$STATE_FILE" ]; then
    STATE=$(cat "$STATE_FILE")
    LAST_ALERT=$(echo "$STATE" | jq -r '.last_alert // empty' 2>/dev/null || echo "")
    LAST_STEP=$(echo "$STATE" | jq -r '.last_step // 0' 2>/dev/null || echo 0)
else
    LAST_ALERT=""
    LAST_STEP=0
fi

# Check if training process is running
PID=$(pgrep -f "train_lora_simple.py" | head -n1 || true)
if [ -z "$PID" ]; then
    log "❌ Training process NOT running!"
    # Check if log shows completion
    if grep -q "Training completed\|completed successfully\|Epoch.*done\|Training finished" "$LOG_FILE" 2>/dev/null; then
        log "✅ Training appears to have completed (found completion marker in log)."
    else
        log "⚠️ Training process is missing and no completion marker found. Likely crashed."
        # Send Telegram alert via slash handler
        MESSAGE="🚨 TinyLlama Training Alert:\n- Process NOT running\n- No completion marker\n- Check log: $LOG_FILE"
        # Use openclaw agent to send alert
        /home/ubuntu/.npm-global/bin/openclaw agent --agent main --message "$MESSAGE" --thinking low --timeout 30000 2>/dev/null || true
    fi
    exit 1
fi

log "✅ Training process running (PID $PID)"

# Check log for recent activity
if [ ! -f "$LOG_FILE" ]; then
    log "⚠️ Log file not found: $LOG_FILE"
    exit 0
fi

# Get last modification time of log (in seconds)
LAST_MOD=$(stat -c %Y "$LOG_FILE" 2>/dev/null || stat -f %m "$LOG_FILE")
NOW=$(date +%s)
AGE_MIN=$(( (NOW - LAST_MOD) / 60 ))

if [ $AGE_MIN -gt 30 ]; then
    log "⚠️ Log hasn't been updated for ${AGE_MIN} minutes (stale check)"
    # Possibly hung; send alert if not recently alerted
    if [ -z "$LAST_ALERT" ] || [ $(( (NOW - LAST_ALERT) / 60 )) -gt $ALERT_COOLDOWN ]; then
        MESSAGE="🚨 TinyLlama Training Stale:\n- No log updates for ${AGE_MIN} minutes\n- Process PID $PID still running\n- Check for hang"
        /home/ubuntu/.npm-global/bin/openclaw agent --agent main --message "$MESSAGE" --thinking low --timeout 30000 2>/dev/null || true
        LAST_ALERT=$NOW
    fi
else
    log "📝 Log active (last update ${AGE_MIN}m ago)"
fi

# Check for error patterns in recent log lines
ERROR_COUNT=$(tail -n 200 "$LOG_FILE" 2>/dev/null | grep -ciE "error|exception|traceback|oom|killed|cuda error|runtime error" || true)
if [ "$ERROR_COUNT" -gt 0 ]; then
    log "🚨 Detected $ERROR_COUNT error lines in recent log"
    # Send alert if not recently sent
    if [ -z "$LAST_ALERT" ] || [ $(( (NOW - LAST_ALERT) / 60 )) -gt $ALERT_COOLDOWN ]; then
        MESSAGE="🚨 TinyLlama Training Errors:\n- Found $ERROR_COUNT error/exception lines in recent log\n- Check: $LOG_FILE"
        /home/ubuntu/.npm-global/bin/openclaw agent --agent main --message "$MESSAGE" --thinking low --timeout 30000 2>/dev/null || true
        LAST_ALERT=$NOW
    fi
else
    log "✅ No errors in recent log"
fi

# Extract progress: last step count
CURRENT_STEP=$(tail -n 100 "$LOG_FILE" 2>/dev/null | grep -Eo '[0-9]+/[0-9]+' | tail -n1 | cut -d/ -f1 || echo "$LAST_STEP")
if [ -n "$CURRENT_STEP" ] && [ "$CURRENT_STEP" -ne "$LAST_STEP" ]; then
    log "📈 Progress: step $CURRENT_STEP"
    LAST_STEP=$CURRENT_STEP
fi

# Save state
echo "{\"last_alert\": $LAST_ALERT, \"last_step\": $LAST_STEP}" > "$STATE_FILE"

exit 0
