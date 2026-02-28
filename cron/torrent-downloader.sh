#!/bin/bash
# Random torrent downloader: pick a random torrent from top 20 (max 1GB) and add to aria2
# Runs every 2h via cron — avoids duplicates via aria2 queue check + history log

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE"

LOG() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | logger -t torrent-downloader; echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }
RPC_SECRET="openclaw_secret_123"
RPC_URL="http://localhost:6800/jsonrpc"
HISTORY_FILE="$WORKSPACE/memory/torrent-history.txt"
LIMIT=20
touch "$HISTORY_FILE"

# Check free space (skip if >90% used)
FREE_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')
if (( FREE_PCT >= 90 )); then
  LOG "Low disk space (${FREE_PCT}% used), skipping"
  exit 0
fi

# Get current aria2 hashes (active + waiting) for duplicate check
QUEUE_HASHES=$(curl -s "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.tellActive\",\"params\":[\"token:$RPC_SECRET\",[\"infoHash\"]]}" | \
  python3 -c "import json,sys; r=json.load(sys.stdin).get('result',[]); [print(x.get('infoHash','').lower()) for x in r]" 2>/dev/null || echo "")
QUEUE_HASHES+=$'\n'$(curl -s "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.tellWaiting\",\"params\":[\"token:$RPC_SECRET\",0,100,[\"infoHash\"]]}" | \
  python3 -c "import json,sys; r=json.load(sys.stdin).get('result',[]); [print(x.get('infoHash','').lower()) for x in r]" 2>/dev/null || echo "")

# Shuffle pick order: try random indices until we find one not in queue/history
INDICES=$(python3 -c "import random; l=list(range(1,$((LIMIT+1)))); random.shuffle(l); print(' '.join(map(str,l)))")

for IDX in $INDICES; do
  # Fetch torrent info for this pick
  OUTPUT=$(./quick nyaa-top --limit "$LIMIT" --max-size 1G --pick "$IDX" 2>/dev/null) || continue

  MAGNET=$(echo "$OUTPUT" | grep -E '^Magnet: ' | head -1 | sed 's/^Magnet: //' | tr -d '\r\n')
  NAME=$(echo "$OUTPUT" | grep -E '^Selected #' | head -1 | sed 's/^Selected #[0-9]*: //' | tr -d '\r\n')

  [ -z "$MAGNET" ] && continue

  BTIH=$(echo "$MAGNET" | grep -oP 'btih:\K[a-fA-F0-9]+' | head -1 | tr '[:upper:]' '[:lower:]' || echo "")
  [ -z "$BTIH" ] && continue

  # Skip if already in aria2 queue
  if echo "$QUEUE_HASHES" | grep -qi "^${BTIH}$" 2>/dev/null; then
    LOG "Already in queue: $NAME, trying next..."
    continue
  fi

  # Skip if in history (already downloaded before)
  if grep -qi "$BTIH" "$HISTORY_FILE" 2>/dev/null; then
    LOG "Already downloaded before: $NAME, trying next..."
    continue
  fi

  # Add to aria2!
  LOG "Adding: $NAME"
  RESULT=$(curl -s "$RPC_URL" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.addUri\",\"params\":[\"token:$RPC_SECRET\",[\"$MAGNET\"]]}")
  GID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('result',''))" 2>/dev/null || echo "")

  if [ -n "$GID" ] && [ "$GID" != "null" ]; then
    LOG "✓ Added GID=$GID: $NAME"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $BTIH $NAME" >> "$HISTORY_FILE"
    exit 0
  else
    LOG "aria2 rejected: $RESULT"
  fi
done

LOG "No new torrents to add (all already queued or downloaded)"
exit 0
