#!/usr/bin/env bash
set -euo pipefail
# Check LinkedIn PA posts for word count below threshold (default 300).
# Lists files that are too short.

THRESHOLD=${1:-300}
WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "Scanning content/2026-02-26-*-linkedin-pa-post.md for posts < $THRESHOLD words..."

find content/ -name '2026-02-26-*-linkedin-pa-post.md' | while read -r file; do
  wc -w < "$file" | {
    read -r words
    if [ "$words" -lt "$THRESHOLD" ]; then
      echo "$file: $words words"
    fi
  }
done
