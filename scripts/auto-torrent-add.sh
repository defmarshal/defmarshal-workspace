#!/usr/bin/env bash
# Auto-torrent adder: pick a random torrent from top 10 (max 2GB) and add to aria2
# Used by auto-torrent-cron (2 AM daily) — now with duplicate prevention
set -euo pipefail
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"
LOG_FILE="$WORKSPACE/memory/auto-torrent.log"
HISTORY_FILE="$WORKSPACE/memory/torrent-history.txt"
RPC_SECRET="openclaw_secret_123"
RPC_URL="http://localhost:6800/jsonrpc"
touch "$HISTORY_FILE"

LOG() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG_FILE"; }

# Get aria2 queue hashes
QUEUE_HASHES=$(curl -s "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.tellActive\",\"params\":[\"token:$RPC_SECRET\",[\"infoHash\"]]}" | \
  python3 -c "import json,sys; [print(x.get('infoHash','').lower()) for x in json.load(sys.stdin).get('result',[])]" 2>/dev/null || echo "")
QUEUE_HASHES+=$'\n'$(curl -s "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.tellWaiting\",\"params\":[\"token:$RPC_SECRET\",0,100,[\"infoHash\"]]}" | \
  python3 -c "import json,sys; [print(x.get('infoHash','').lower()) for x in json.load(sys.stdin).get('result',[])]" 2>/dev/null || echo "")

# Try random picks from top 10
INDICES=$(python3 -c "import random; l=list(range(1,11)); random.shuffle(l); print(' '.join(map(str,l)))")
for IDX in $INDICES; do
  OUTPUT=$(./quick nyaa-top --limit 10 --max-size 2G --pick "$IDX" 2>/dev/null) || continue
  MAGNET=$(echo "$OUTPUT" | grep -E '^Magnet: ' | head -1 | sed 's/^Magnet: //' | tr -d '\r\n')
  NAME=$(echo "$OUTPUT" | grep -E '^Selected #' | head -1 | sed 's/^Selected #[0-9]*: //')
  [ -z "$MAGNET" ] && continue
  BTIH=$(echo "$MAGNET" | grep -oP 'btih:\K[a-fA-F0-9]+' | head -1 | tr '[:upper:]' '[:lower:]' || echo "")
  [ -z "$BTIH" ] && continue
  echo "$QUEUE_HASHES" | grep -qi "^${BTIH}$" && { LOG "Already queued: $NAME"; continue; }
  grep -qi "$BTIH" "$HISTORY_FILE" 2>/dev/null && { LOG "Already downloaded: $NAME"; continue; }
  RESULT=$(curl -s "$RPC_URL" -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.addUri\",\"params\":[\"token:$RPC_SECRET\",[\"$MAGNET\"]]}")
  GID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('result',''))" 2>/dev/null || echo "")
  if [ -n "$GID" ] && [ "$GID" != "null" ]; then
    LOG "✓ Added GID=$GID: $NAME"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $BTIH $NAME" >> "$HISTORY_FILE"
    exit 0
  fi
done
LOG "No new torrents to add (all already queued/downloaded)"
