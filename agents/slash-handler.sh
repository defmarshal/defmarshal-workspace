#!/usr/bin/env bash
# slash-handler.sh — Telegram slash command processor
# Polls the main Telegram session for recent slash commands and responds.
# Runs every 2 minutes via OpenClaw cron.
#
# Supported commands:
#   /status   — system summary
#   /health   — health check
#   /downloads — aria2 download status
#   /cron     — cron job list
#   /disk     — disk usage
#   /help     — list commands
#
# Sends responses via: openclaw agent --session-id <id> --message <text> --deliver

set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
SESSION_ID="bcc62cdd-c612-4f74-8f20-559e10b3dad6"
SESSIONS_JSON="$HOME/.openclaw/agents/main/sessions/sessions.json"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
STATE_FILE="$WORKSPACE/memory/.slash-handler-state.json"
LOG="$WORKSPACE/memory/slash-handler.log"

log() { echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $*" >> "$LOG"; }

# ── Resolve the actual session JSONL file for the Telegram direct session ──
resolve_telegram_session() {
  python3 - <<'PYEOF'
import json, os, sys
sessions_json = os.path.expanduser("~/.openclaw/agents/main/sessions/sessions.json")
try:
    with open(sessions_json) as f:
        sessions = json.load(f)
    # Look for a Telegram direct session key
    for key, val in sessions.items():
        if 'telegram' in key.lower() and 'direct' in key.lower():
            print(val.get('sessionId', ''))
            sys.exit(0)
except Exception as e:
    pass
sys.exit(1)
PYEOF
}

# ── Get last user message from a session JSONL ──
get_last_user_message() {
  local session_file="$1"
  python3 - "$session_file" <<'PYEOF'
import json, sys, re
fname = sys.argv[1]
last_msg = None
last_ts = None
def iso_to_ts(s):
    # Convert ISO 8601 to float timestamp; return 0 if invalid
    try:
        # Handle both string and numeric timestamps
        if isinstance(s, (int, float)):
            return float(s)
        if not s:
            return 0.0
        # Parse ISO string like "2026-03-15T14:41:19.877Z"
        # Remove Z and split
        s = s.replace('Z', '')
        if 'T' in s:
            date_part, time_part = s.split('T', 1)
            y, m, d = date_part.split('-')
            h, mi, sec = time_part.split(':', 2)
            s_val = float(sec) if '.' not in sec else float(sec)
            # Build timestamp (rough but consistent)
            import datetime
            dt = datetime.datetime(int(y), int(m), int(d), int(h), int(mi), int(sec.split('.')[0]), 
                                  int(sec.split('.')[1].ljust(6, '0')[:6]) if '.' in sec else 0)
            return dt.timestamp()
    except:
        return 0.0
    return 0.0

try:
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue
            if obj.get('type') == 'message' and obj.get('message', {}).get('role') == 'user':
                raw_ts = obj.get('timestamp', 0)
                ts = iso_to_ts(raw_ts)
                if last_ts is None or ts > last_ts:
                    last_ts = ts
                    content = obj['message'].get('content', '')
                    if isinstance(content, list):
                        texts = [c['text'] for c in content if c.get('type') == 'text']
                        content = ' '.join(texts)
                    last_msg = (content or '').strip()
                    last_ts_out = ts
    if last_msg and last_ts:
        print(json.dumps({'text': last_msg, 'ts': last_ts}))
except Exception as e:
    pass
PYEOF
}

# ── Load/save state to avoid re-processing same message ──
get_last_processed_ts() {
  python3 -c "
import json
try:
    with open('$STATE_FILE') as f:
        d = json.load(f)
    print(d.get('last_ts', 0))
except:
    print(0)
"
}

save_last_processed_ts() {
  local ts="$1"
  python3 -c "
import json
with open('$STATE_FILE', 'w') as f:
    json.dump({'last_ts': $ts}, f)
"
}

# ── Command handlers ──
cmd_status() {
  cd "$WORKSPACE"
  ./quick status 2>/dev/null || echo "status unavailable"
}

cmd_health() {
  cd "$WORKSPACE"
  ./quick health 2>/dev/null || echo "health unavailable"
}

cmd_downloads() {
  cd "$WORKSPACE"
  # Use the aria2 RPC to get active downloads
  local result
  result=$(python3 - <<'PYEOF' 2>/dev/null
import urllib.request, json

def aria2(method, params=[]):
    body = json.dumps({"jsonrpc":"2.0","method":method,"id":"1","params":["token:openclaw_secret_123"]+params}).encode()
    try:
        req = urllib.request.Request("http://localhost:6800/jsonrpc",
            data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read()).get("result", [])
    except:
        return []

fields = ["gid","status","totalLength","completedLength","downloadSpeed","files","bittorrent"]
active = aria2("aria2.tellActive", [fields])

def fmt_bytes(n):
    n = int(n) if n else 0
    if n > 1e9: return f"{n/1e9:.1f} GB"
    if n > 1e6: return f"{n/1e6:.1f} MB"
    if n > 1e3: return f"{n/1e3:.1f} KB"
    return f"{n} B"

if not active:
    print("No active downloads.")
else:
    lines = ["📥 Active downloads:"]
    for it in active[:5]:
        name = (it.get("bittorrent") or {}).get("info",{}).get("name","")
        if not name:
            files = it.get("files", [])
            if files:
                name = files[0].get("path","").split("/")[-1] or it["gid"]
        total = int(it.get("totalLength",0) or 0)
        done  = int(it.get("completedLength",0) or 0)
        pct   = f"{done/total*100:.0f}%" if total > 0 else "?"
        speed = fmt_bytes(it.get("downloadSpeed",0)) + "/s"
        lines.append(f"• {name[:40]} — {pct} @ {speed}")
    print("\n".join(lines))
PYEOF
  )
  echo "${result:-No active downloads}"
}

cmd_cron() {
  local cron_json
  cron_json=$(openclaw cron list --json 2>/dev/null || echo "[]")
  python3 - <<PYEOF
import json, sys
try:
    jobs = json.loads('''$cron_json''')
    if not jobs:
        print("No cron jobs.")
        sys.exit(0)
    lines = ["⏰ Cron jobs:"]
    for j in jobs[:15]:
        name = j.get("name", j.get("id","?"))
        sched = j.get("schedule", {})
        expr = sched.get("expr", "?") if isinstance(sched, dict) else str(sched)
        state = j.get("state", {})
        status = state.get("lastStatus", state.get("lastRunStatus", "?"))
        enabled = "✓" if j.get("enabled", True) else "✗"
        lines.append(f"{enabled} {name} — {expr} [{status}]")
    print("\n".join(lines))
except Exception as e:
    print(f"Could not load cron jobs: {e}")
PYEOF
}

cmd_disk() {
  df -h / "$WORKSPACE" 2>/dev/null | awk '
    NR==1 { print "💾 Disk usage:" }
    NR>1  { printf "  %s: %s used / %s total (%s)\n", $6, $3, $2, $5 }
  '
}

cmd_help() {
  cat <<'EOF'
🤖 Slash commands available:
  /status     — system summary
  /health     — health check
  /downloads  — active aria2 downloads
  /cron       — cron job list
  /disk       — disk usage
  /help       — this message
EOF
}

# ── Deliver a response to Telegram ──
deliver() {
  local msg="$1"
  # Truncate to safe length
  if [ ${#msg} -gt 3800 ]; then
    msg="${msg:0:3800}…"
  fi
  openclaw agent \
    --session-id "$SESSION_ID" \
    --message "$msg" \
    --deliver \
    2>>"$LOG" || true
}

# ── Main ──
main() {
  log "Slash handler running"

  # Resolve session file
  local session_id
  session_id=$(resolve_telegram_session 2>/dev/null || echo "$SESSION_ID")
  local session_file="$SESSIONS_DIR/${session_id}.jsonl"

  if [ ! -f "$session_file" ]; then
    # Try the hardcoded session ID as fallback
    session_file="$SESSIONS_DIR/${SESSION_ID}.jsonl"
  fi

  if [ ! -f "$session_file" ]; then
    log "ERROR: session file not found: $session_file"
    exit 0
  fi

  # Get last user message
  local msg_json
  msg_json=$(get_last_user_message "$session_file" 2>/dev/null || echo "")
  if [ -z "$msg_json" ]; then
    log "No user messages found"
    exit 0
  fi

  local msg_text msg_ts
  msg_text=$(python3 -c "import json,sys; d=json.loads('''$msg_json'''); print(d['text'])" 2>/dev/null || echo "")
  msg_ts=$(python3 -c "import json,sys; d=json.loads('''$msg_json'''); print(d['ts'])" 2>/dev/null || echo "0")

  # Check if it's a slash command
  if [[ "$msg_text" != /* ]]; then
    log "Last message is not a slash command: ${msg_text:0:40}"
    exit 0
  fi

  # Check we haven't already processed this message
  local last_ts
  last_ts=$(get_last_processed_ts)
  if [ "$msg_ts" -le "$last_ts" ] 2>/dev/null; then
    log "Already processed ts=$msg_ts (last=$last_ts)"
    exit 0
  fi

  # Extract command word (strip leading /)
  local cmd args
  cmd=$(echo "$msg_text" | awk '{print $1}' | tr -d '/' | tr '[:upper:]' '[:lower:]')
  args=$(echo "$msg_text" | cut -d' ' -f2- 2>/dev/null || echo "")

  log "Processing slash command: /$cmd (ts=$msg_ts)"

  # Route command
  local response
  case "$cmd" in
    status)    response=$(cmd_status) ;;
    health)    response=$(cmd_health) ;;
    downloads) response=$(cmd_downloads) ;;
    cron)      response=$(cmd_cron) ;;
    disk)      response=$(cmd_disk) ;;
    help)      response=$(cmd_help) ;;
    *)         response="Unknown command: /$cmd — try /help" ;;
  esac

  log "Delivering response for /$cmd (${#response} chars)"
  deliver "$response"

  # Save processed timestamp
  save_last_processed_ts "$msg_ts"
  log "Done"
}

main "$@"
