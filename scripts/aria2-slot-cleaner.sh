#!/bin/bash
# aria2-slot-cleaner: remove 100%-complete torrents from active queue so slots stay free
# Run every 5 min via system crontab

RPC_URL="http://localhost:6800/jsonrpc"
SECRET="openclaw_secret_123"

GIDS=$(curl -s "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.tellActive\",\"params\":[\"token:$SECRET\",[\"gid\",\"totalLength\",\"completedLength\"]]}" | \
  python3 -c "
import json,sys
r=json.load(sys.stdin).get('result',[])
for x in r:
    t=int(x.get('totalLength',0)); c=int(x.get('completedLength',0))
    if t>0 and c>=t: print(x['gid'])
" 2>/dev/null)

[ -z "$GIDS" ] && exit 0

for GID in $GIDS; do
  curl -s "$RPC_URL" -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"aria2.remove\",\"params\":[\"token:$SECRET\",\"$GID\"]}" > /dev/null
  logger -t aria2-cleaner "Removed completed GID=$GID"
done
