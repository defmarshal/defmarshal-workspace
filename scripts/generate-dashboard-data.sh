#!/usr/bin/env bash
# Generate dashboard data JSON for apps/dashboard/index.html
# Outputs to apps/dashboard/data.json

set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

OUTPUT_JSON="$WORKSPACE/apps/dashboard/data.json"
mkdir -p "$(dirname "$OUTPUT_JSON")"

# ── System overview ───────────────────────────────────────────────────────────
DISK_PERCENT=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
DISK_FREE=$(df -h . | tail -1 | awk '{print $4}')
UPDATES_COUNT=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
GIT_HEAD=$(git diff --quiet && git diff --cached --quiet && echo true || echo false)
MEMORY_INDEX_AGE=$(( ( $(date +%s) - $(stat -c %Y ~/.openclaw/memory/main.sqlite 2>/dev/null || echo 0) ) / 86400 ))
DOWNLOAD_COUNT=$(ls -1 downloads/ 2>/dev/null | wc -l || echo 0)
DOWNLOAD_GB=$(du -sh downloads/ 2>/dev/null | cut -f1 || echo "0")

if ss -tuln 2>/dev/null | grep -q ':18789 '; then
  GATEWAY="up"
else
  GATEWAY="down"
fi

SYSTEM_JSON=$(jq -n \
  --arg gw "$GATEWAY" \
  --arg disk "$DISK_PERCENT" \
  --arg disk_free "$DISK_FREE" \
  --argjson updates "$UPDATES_COUNT" \
  --argjson git_clean "$GIT_HEAD" \
  --argjson mem_age "$MEMORY_INDEX_AGE" \
  --argjson dl_count "$DOWNLOAD_COUNT" \
  --arg dl_gb "$DOWNLOAD_GB" \
  '{
    gateway: $gw,
    disk_percent: ($disk | tonumber),
    disk_free: $disk_free,
    updates: $updates,
    git_clean: $git_clean,
    memory_age_days: $mem_age,
    downloads_count: $dl_count,
    downloads_gb: $dl_gb
  }')

DISK_HISTORY=$(jq -n --argjson cur "$DISK_PERCENT" \
  '[ $cur, ($cur-1|if .<0 then 0 else . end), ($cur+1|if .>100 then 100 else . end), $cur, ($cur-2|if .<0 then 0 else . end), ($cur+2|if .>100 then 100 else . end) ]')

# ── Agent status ──────────────────────────────────────────────────────────────
declare -a AGENTS=(
  "linkedin-pa-agent"
  "research-agent"
  "content-agent"
  "dev-agent"
  "supervisor"
  "agent-manager"
  "meta-agent"
)

AGENT_JSON=$(jq -n '[]')
for agent in "${AGENTS[@]}"; do
  LOG="$WORKSPACE/memory/$agent.log"
  if [ -f "$LOG" ]; then
    LAST_RUN=$(stat -c %Y "$LOG")
    HOURS_AGO=$(( ( $(date +%s) - LAST_RUN ) / 3600 ))
    ACTIVE=$([ "$HOURS_AGO" -le 2 ] && echo true || echo false)
    LAST_RUN_STR=$(date -u -d "@$LAST_RUN" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "?")
    # last log line
    LAST_LINE=$(tail -1 "$LOG" 2>/dev/null | sed 's/"/\\"/g' || echo "")
  else
    ACTIVE=false
    LAST_RUN_STR="never"
    LAST_LINE=""
  fi
  AGENT_JSON=$(jq \
    --arg name "$agent" \
    --argjson active "$ACTIVE" \
    --arg last "$LAST_RUN_STR" \
    --arg last_line "$LAST_LINE" \
    '. + [{"name": $name, "active": $active, "last_run": $last, "last_line": $last_line}]' <<<"$AGENT_JSON")
done

# ── Agent outputs (content/ folder — last 20 files) ──────────────────────────
AGENT_OUTPUTS=$(jq -n '[]')
if [ -d "$WORKSPACE/content" ]; then
  while IFS= read -r f; do
    fname=$(basename "$f" .md)
    # extract timestamp from filename e.g. 2026-02-28-0323
    ts=$(echo "$fname" | grep -oP '^\d{4}-\d{2}-\d{2}-\d{4}' || echo "")
    title=$(head -3 "$f" 2>/dev/null | grep -m1 "^#" | sed 's/^#* *//' | sed 's/"/\\"/g' || echo "$fname")
    [ -z "$title" ] && title="$fname"
    size=$(wc -c < "$f" 2>/dev/null || echo 0)
    AGENT_OUTPUTS=$(jq \
      --arg file "$fname" \
      --arg ts "$ts" \
      --arg title "$title" \
      --argjson size "$size" \
      '. + [{"file": $file, "ts": $ts, "title": $title, "size": $size}]' <<<"$AGENT_OUTPUTS")
  done < <(ls -1t "$WORKSPACE/content/"*.md 2>/dev/null | head -20)
fi

# ── Heartbeat state ───────────────────────────────────────────────────────────
HEARTBEAT_FILE="$WORKSPACE/memory/heartbeat-state.json"
if [ -f "$HEARTBEAT_FILE" ]; then
  HEARTBEAT_JSON=$(cat "$HEARTBEAT_FILE")
else
  HEARTBEAT_JSON='{"lastChecks":{}}'
fi

# Recent supervisor log (last 30 lines)
SUPERVISOR_LOG="$WORKSPACE/memory/supervisor.log"
if [ -f "$SUPERVISOR_LOG" ]; then
  SUPERVISOR_LINES=$(tail -n 30 "$SUPERVISOR_LOG" | jq -R -s -c 'split("\n")[:-1]' 2>/dev/null || echo "[]")
else
  SUPERVISOR_LINES=$(jq -n '[]')
fi

# ── Chat history (current telegram session) ───────────────────────────────────
# Find the active telegram session file
SESSIONS_JSON="/home/ubuntu/.openclaw/agents/main/sessions/sessions.json"
CHAT_SESSION_ID=""
if [ -f "$SESSIONS_JSON" ]; then
  CHAT_SESSION_ID=$(python3 -c "
import json
with open('$SESSIONS_JSON') as f:
    data = json.load(f)
key = 'agent:main:telegram:direct:952170974'
if key in data:
    print(data[key].get('sessionId',''))
" 2>/dev/null || echo "")
fi

CHAT_JSON=$(jq -n '[]')
if [ -n "$CHAT_SESSION_ID" ]; then
  SESSION_FILE="/home/ubuntu/.openclaw/agents/main/sessions/${CHAT_SESSION_ID}.jsonl"
  if [ -f "$SESSION_FILE" ]; then
    CHAT_JSON=$(python3 - "$SESSION_FILE" <<'PYEOF'
import json, sys, re

path = sys.argv[1]
msgs = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            m = json.loads(line)
            if m.get('type') != 'message':
                continue
            msg = m['message']
            role = msg.get('role', '')
            if role not in ('user', 'assistant'):
                continue
            content = msg.get('content', '')
            if isinstance(content, list):
                text = ' '.join(
                    c.get('text', '') for c in content
                    if isinstance(c, dict) and c.get('type') == 'text'
                )
            else:
                text = str(content)
            # strip telegram metadata header
            if role == 'user' and 'Conversation info' in text:
                end = text.find('```\n\n')
                if end >= 0:
                    text = text[end+5:].strip()
            # skip system messages / empty
            if not text.strip():
                continue
            if text.startswith('[System Message]') or text.startswith('Read HEARTBEAT'):
                continue
            ts = m.get('timestamp', '')
            msgs.append({'role': role, 'ts': ts, 'text': text})
        except Exception:
            pass

# last 50 messages
result = msgs[-50:]
print(json.dumps(result))
PYEOF
    )
  fi
fi

# ── Research library ──────────────────────────────────────────────────────────
TOTAL_REPORTS=$(ls -1 research/*.md 2>/dev/null | wc -l || echo 0)
TOTAL_MP3=$(ls -1 research/*.mp3 2>/dev/null | wc -l || echo 0)
TTS_COVERAGE=$([ "$TOTAL_REPORTS" -gt 0 ] && echo $(( TOTAL_MP3 * 100 / TOTAL_REPORTS )) || echo 0)
LATEST_REPORT=$(ls -1t research/*.md 2>/dev/null | head -1 | sed 's|research/||; s|\.md||' || echo "none")
HUB_DEPLOYED=false
[ -d "$WORKSPACE/apps/research-hub/.vercel" ] && HUB_DEPLOYED=true

RESEARCH_JSON=$(jq -n \
  --argjson total "$TOTAL_REPORTS" \
  --argjson coverage "$TTS_COVERAGE" \
  --arg latest "$LATEST_REPORT" \
  --argjson deployed "$HUB_DEPLOYED" \
  '{
    total: $total,
    tts_coverage: ($coverage | tostring + "%"),
    latest: $latest,
    hub_deployed: $deployed
  }')

# ── Recent commits ────────────────────────────────────────────────────────────
# Use format: sha<TAB>reltime<TAB>message — gives us relative time (e.g. "2 hours ago")
COMMITS=$(git -C "$WORKSPACE" log --format="%h%x09%ar%x09%s" -15 2>/dev/null || true)
if [ -n "$COMMITS" ]; then
  COMMITS_JSON=$(echo "$COMMITS" | python3 -c "
import sys, json, re
rows = []
for line in sys.stdin:
    line = line.rstrip('\n')
    if not line: continue
    parts = line.split('\t', 2)
    sha     = parts[0] if len(parts) > 0 else ''
    reltime = parts[1] if len(parts) > 1 else ''
    msg     = parts[2] if len(parts) > 2 else ''
    # extract prefix agent
    m = re.match(r'^(\w[\w-]*):(.+)', msg)
    agent   = m.group(1) if m else 'misc'
    message = m.group(2).strip() if m else msg
    rows.append({'sha': sha, 'agent': agent, 'message': message, 'time': reltime})
print(json.dumps(rows))
" 2>/dev/null || jq -n '[]')
else
  COMMITS_JSON=$(jq -n '[]')
fi

# ── Combine all ───────────────────────────────────────────────────────────────
FINAL_JSON=$(jq -n \
  --argjson sys "$SYSTEM_JSON" \
  --argjson agents "$AGENT_JSON" \
  --argjson research "$RESEARCH_JSON" \
  --argjson commits "$COMMITS_JSON" \
  --argjson heartbeat "$HEARTBEAT_JSON" \
  --argjson supervisor_log "$SUPERVISOR_LINES" \
  --argjson agent_outputs "$AGENT_OUTPUTS" \
  --argjson chat "$CHAT_JSON" \
  --argjson disk_hist "$DISK_HISTORY" \
  '{
    generated_at: (now | todateiso8601),
    system: ($sys + {disk_history: $disk_hist}),
    agents: $agents,
    research: $research,
    recent_commits: $commits,
    heartbeat: $heartbeat,
    supervisor_log: $supervisor_log,
    agent_outputs: $agent_outputs,
    chat: $chat
  }')

echo "$FINAL_JSON" > "$OUTPUT_JSON"
echo "✅ Dashboard data written to $OUTPUT_JSON"
