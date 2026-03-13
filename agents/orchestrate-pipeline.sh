#!/usr/bin/env bash
set -euo pipefail

cd "/home/ubuntu/.openclaw/workspace"

LOGFILE="memory/orchestrator-pipeline.log"
mkdir -p memory

log() {
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $*" | tee -a "$LOGFILE"
}

log "=== Orchestrator Pipeline Starting ==="

# Step 1: Find latest research report
LATEST_RESEARCH=$(ls -t research/2026-03-*.md 2>/dev/null | head -1 || true)
if [ -z "$LATEST_RESEARCH" ]; then
  log "❌ No research report found for today. Aborting."
  exit 1
fi
log "📄 Latest research: $LATEST_RESEARCH"

# Step 2: Extract title/topic (first line, remove date prefix)
TOPIC=$(head -1 "$LATEST_RESEARCH" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}[[:space:]]*//' | sed 's/\.md$//')
log "🎯 Topic extracted: $TOPIC"

# Step 3: Spawn content-agent with topic context
log "🚀 Spawning content-agent to write about: $TOPIC"
openclaw agent --agent main --message "You are the content-agent. Write a comprehensive blog post (800-1500 words) about: $TOPIC. Include an engaging introduction, reasoned sections, and a conclusion. Use markdown format. Save to content/ with filename: 2026-03-13-blog-$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]_-' | cut -c1-50).md" --timeout 600000 >> "$LOGFILE" 2>&1 || {
  log "❌ Content-agent failed"
  exit 1
}
log "✅ Content-agent completed"

# Step 4: Spawn dev-agent to create a related feature
log "🚀 Spawning dev-agent to implement complementary feature for: $TOPIC"
openclaw agent --agent qwen --message "You are dev-agent. Based on the research topic '$TOPIC', create a simple Python script or HTML page that visualizes or demonstrates a key concept from that topic. Target: quick prototype, not production. Save to apps/ or scripts/ with descriptive name. Make it usable and show sample output in comments." --timeout 600000 >> "$LOGFILE" 2>&1 || {
  log "❌ Dev-agent failed"
  exit 1
}
log "✅ Dev-agent completed"

log "=== Orchestrator Pipeline Complete ==="
