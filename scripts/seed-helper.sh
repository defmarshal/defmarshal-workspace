#!/usr/bin/env bash
# seed-helper.sh — Utility to inspect and filter research seeds
# Usage: ./seed-helper.sh [list|stats|filter <keyword>]

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
SEEDS_FILE="$WORKSPACE/memory/seeds.jsonl"
PROCESSED_FILE="$WORKSPACE/memory/processed_seeds.jsonl"

cmd="${1:-list}"
shift || true

list_seeds() {
    echo "=== Research Seeds Overview ==="
    echo ""
    echo "Total seeds:"
    wc -l < "$SEEDS_FILE"
    echo "Processed seeds:"
    wc -l < "$PROCESSED_FILE" 2>/dev/null || echo "0"
    echo "Unprocessed:"
    comm -23 <(sort "$SEEDS_FILE" | cut -d'"' -f4) <(sort "$PROCESSED_FILE" | cut -d'"' -f4) 2>/dev/null | wc -l
    echo ""
    echo "Top 10 most recent seeds:"
    python3 -c "
import json, sys, datetime
with open('$SEEDS_FILE') as f:
    seeds = [json.loads(line) for line in f if line.strip()]
seeds.sort(key=lambda x: x.get('ts',''), reverse=True)
for s in seeds[:10]:
    print(f\"- {s.get('title','')[:80]}... ({s.get('source','')})\")
"
}

filter_seeds() {
    keyword="$1"
    echo "=== Seeds containing '$keyword' ==="
    python3 -c "
import json, sys
keyword = '$keyword'.lower()
with open('$SEEDS_FILE') as f:
    seeds = [json.loads(line) for line in f if line.strip()]
matches = [s for s in seeds if keyword in s.get('title','').lower()]
print(f'Found {len(matches)} matches (showing first 20):')
for s in sorted(matches, key=lambda x: x.get('ts',''), reverse=True)[:20]:
    print(f\"- {s.get('title','')[:80]}... ({s.get('source','')})\")
"
}

stats() {
    echo "=== Seed Statistics ==="
    echo ""
    echo "By source (top 10):"
    python3 -c "
import json, collections, sys
with open('$SEEDS_FILE') as f:
    seeds = [json.loads(line) for line in f if line.strip()]
counts = collections.Counter(s.get('source','') for s in seeds)
for src, cnt in counts.most_common(10):
    print(f'  {src}: {cnt}')
"
    echo ""
    echo "By tag (top 10):"
    python3 -c "
import json, collections, sys
with open('$SEEDS_FILE') as f:
    seeds = [json.loads(line) for line in f if line.strip()]
tag_counts = collections.Counter()
for s in seeds:
    for t in s.get('tags',[]):
        tag_counts[t] += 1
for tag, cnt in tag_counts.most_common(10):
    print(f'  {tag}: {cnt}')
"
}

case "$cmd" in
    list)
        list_seeds
        ;;
    stats)
        stats
        ;;
    filter)
        if [ -z "$*" ]; then
            echo "Usage: $0 filter <keyword>"
            exit 1
        fi
        filter_seeds "$*"
        ;;
    *)
        echo "Usage: $0 {list|stats|filter <keyword>}"
        exit 1
        ;;
esac
