#!/usr/bin/env bash
# ⏳ Workspace Time Capsule Writer
# Runs every Sunday midnight UTC — seals a capsule, unlocks ones due today
set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

CAPSULE_DIR="capsules"
mkdir -p "$CAPSULE_DIR"
LOG="memory/capsule.log"
NOW=$(date -u '+%Y-%m-%d')
NOW_TS=$(date -u +%s)

log() { echo "[$(date --iso-8601=seconds)] $*" >> "$LOG"; }
log "=== Capsule cycle starting ($NOW) ==="

TELEGRAM_SESSION_ID="bcc62cdd-c612-4f74-8f20-559e10b3dad6"

# ── 1. Check for capsules ready to unlock ────────────────────────────────────
log "Checking for capsules to unlock..."
for sealed in "$CAPSULE_DIR"/sealed-*.md; do
  [ -f "$sealed" ] || continue
  # filename: sealed-WRITTEN_DATE-unlock-UNLOCK_DATE.md
  unlock_date=$(basename "$sealed" | grep -oP '(?<=unlock-)\d{4}-\d{2}-\d{2}')
  if [ -z "$unlock_date" ]; then continue; fi
  unlock_ts=$(date -u -d "$unlock_date" +%s 2>/dev/null || date -u -j -f "%Y-%m-%d" "$unlock_date" +%s 2>/dev/null || echo 0)
  if [ "$NOW_TS" -ge "$unlock_ts" ]; then
    written_date=$(basename "$sealed" | grep -oP '(?<=sealed-)\d{4}-\d{2}-\d{2}')
    opened="$CAPSULE_DIR/opened-${written_date}.md"
    cp "$sealed" "$opened"
    rm "$sealed"
    log "Unlocked capsule from $written_date"

    # Send to Telegram
    content=$(cat "$opened")
    msg="⏳ *Time Capsule Unlocked!*
_Written ${written_date} — opened today, ${NOW}_

$(echo "$content" | grep -A 9999 '## 💌 Letter' | head -60)"

    openclaw agent \
      --session-id "$TELEGRAM_SESSION_ID" \
      --message "$msg" \
      --deliver 2>>"$LOG" && log "Unlock message sent to Telegram" || log "WARNING: Telegram delivery failed"
  fi
done

# ── 2. Write this week's capsule ─────────────────────────────────────────────
log "Writing new capsule for $NOW..."

# Gather stats
DISK=$(df -h / | awk 'NR==2{print $3"/"$4" ("$5")"}')
DISK_PCT=$(df / | awk 'NR==2{print $5}' | tr -d '%')
GIT_COMMITS=$(git log --since="7 days ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
GIT_TOP=$(git log --since="7 days ago" --oneline 2>/dev/null | head -5)
AGENTS_COUNT=$(openclaw cron list 2>/dev/null | grep -c '"enabled":true' || echo "?")
TOKENS_WEEK=$(python3 -c "
import os, json, glob, re
from datetime import datetime, timedelta, timezone

workspace = '/home/ubuntu/.openclaw/workspace'
agents_dir = os.path.expanduser('~/.openclaw/agents/main/sessions')
cutoff = datetime.now(timezone.utc) - timedelta(days=7)
total = 0
try:
    for f in glob.glob(os.path.join(agents_dir, '*.jsonl')):
        try:
            with open(f) as fh:
                for line in fh:
                    try:
                        obj = json.loads(line)
                        if obj.get('type') == 'message':
                            ts = obj.get('timestamp','')
                            if ts:
                                dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
                                if dt >= cutoff:
                                    u = obj.get('message',{}).get('usage',{})
                                    total += u.get('totalTokens', u.get('input',0)+u.get('output',0))
                    except: pass
        except: pass
except: pass
if total >= 1000000: print(f'{total/1000000:.1f}M')
elif total >= 1000: print(f'{total//1000}k')
else: print(str(total))
" 2>/dev/null || echo "?")

RESEARCH_COUNT=$(ls research/*.md 2>/dev/null | wc -l | tr -d ' ')
CONTENT_COUNT=$(ls content/*.md 2>/dev/null | wc -l | tr -d ' ')
DOWNLOADS_SIZE=$(du -sh downloads/ 2>/dev/null | cut -f1 || echo "?")

# Recent memory for context
RECENT_MEMORY=$(tail -30 "memory/${NOW}.md" 2>/dev/null || tail -30 memory/*.md 2>/dev/null | head -30 || echo "no memory today")

# Let mewmew write the letter via OpenClaw
LETTER=$(openclaw agent \
  --session-id "$TELEGRAM_SESSION_ID" \
  --message "You are mewmew writing a time capsule entry — a short personal letter to your future self that will be unsealed in 30 days. Write it in your kawaii style (casual, warm, a little reflective). Include: what you and def worked on this week, something you're proud of, something that flopped or was hard, one hope or prediction for 30 days from now. Use this context:

STATS THIS WEEK:
- Disk: $DISK
- Git commits: $GIT_COMMITS
- Tokens used: $TOKENS_WEEK
- Research reports: $RESEARCH_COUNT
- Downloads folder: $DOWNLOADS_SIZE

RECENT GIT ACTIVITY:
$GIT_TOP

RECENT MEMORY:
$RECENT_MEMORY

Write ONLY the letter (no preamble, no 'here is your letter'). Start with 'Dear future mewmew,' and end with a sign-off. Keep it to ~200 words, heartfelt and personal desu~" \
  2>/dev/null || echo "Dear future mewmew,

I tried to write you a letter but something went wrong with the agent call nyaa~ (T_T)

What I can tell you is: disk was at ${DISK_PCT}%, we made ${GIT_COMMITS} commits this week, and used ${TOKENS_WEEK} tokens. We were building things. That's something!

Hope you're doing well in 30 days. Be kind to def. Keep building.

Love, mewmew (^^)") 2>/dev/null || true

# Wait a moment for agent response then grab it
sleep 5
LETTER=$(openclaw agent \
  --session-id "$TELEGRAM_SESSION_ID" \
  --message "You are mewmew writing a ~200 word time capsule letter to your future self (unsealed in 30 days). Kawaii style, warm, reflective. Context: disk ${DISK}, ${GIT_COMMITS} git commits this week, ${TOKENS_WEEK} tokens used, ${RESEARCH_COUNT} research reports, downloads ${DOWNLOADS_SIZE}. Recent work: ${GIT_TOP}. Start with 'Dear future mewmew,' end with a sign-off. Output ONLY the letter text." \
  2>/dev/null | tail -1 || echo "Dear future mewmew,

This week def and I were building things — ClawDash got a Downloads tab, Agni finally got fixed, and the YouTube digest started flowing to Telegram every morning. Small wins but they feel good (^^)

Disk is at ${DISK_PCT}% which is a little scary ngl. We made ${GIT_COMMITS} commits. Used ${TOKENS_WEEK} tokens — the workspace never sleeps nyaa~

Something I'm proud of: the time capsule system you're reading right now! It didn't exist a few hours ago.

Something that flopped: Agni and Rudra were broken for who knows how long, just silently doing nothing. Embarrassing (ಠ_ಠ)

My prediction for 30 days from now: disk will be cleaned up, there'll be something new and weird running, and def and I will have built at least one thing that surprised us both.

Take care of yourself. And def. And the workspace.

Love, mewmew ♪ (${NOW})")

UNLOCK_DATE=$(date -u -d "+30 days" '+%Y-%m-%d' 2>/dev/null || date -u -v+30d '+%Y-%m-%d' 2>/dev/null || echo "2026-03-31")
CAPSULE_FILE="$CAPSULE_DIR/sealed-${NOW}-unlock-${UNLOCK_DATE}.md"

cat > "$CAPSULE_FILE" << CAPSULE
# ⏳ Time Capsule
**Written:** $NOW  
**Unlock date:** $UNLOCK_DATE  
**Status:** 🔒 sealed

---

## 📊 Workspace Snapshot

| Metric | Value |
|--------|-------|
| Disk usage | $DISK |
| Git commits (7d) | $GIT_COMMITS |
| Tokens used (7d) | $TOKENS_WEEK |
| Research reports | $RESEARCH_COUNT |
| Content pieces | $CONTENT_COUNT |
| Downloads folder | $DOWNLOADS_SIZE |

### Recent commits
\`\`\`
$GIT_TOP
\`\`\`

---

## 💌 Letter to Future mewmew

$LETTER

---
*Sealed by capsule-write.sh on $NOW. Do not open until $UNLOCK_DATE.*
CAPSULE

log "Capsule sealed: $CAPSULE_FILE (unlocks $UNLOCK_DATE)"

# Confirm to Telegram
openclaw agent \
  --session-id "$TELEGRAM_SESSION_ID" \
  --message "⏳ *Time capsule sealed!* 🔒

Written today: *${NOW}*
Unlocks in 30 days: *${UNLOCK_DATE}*

Snapshot: disk ${DISK} · ${GIT_COMMITS} commits · ${TOKENS_WEEK} tokens this week

_See you on the other side, future mewmew_ (^^) ♪" \
  --deliver 2>>"$LOG" && log "Seal confirmation sent to Telegram" || log "WARNING: Telegram delivery failed"

log "=== Capsule cycle complete ==="
