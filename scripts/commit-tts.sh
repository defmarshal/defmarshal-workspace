#!/usr/bin/env bash
set -euo pipefail
# Commit newly generated TTS audio files (research/*.mp3) that are not yet tracked.
# Useful as a post‑TTS step or periodic cron job.

WORKSPACE="/home/ubuntu/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# Find untracked .mp3 files in research/
UNTRACKED_MP3=$(git status --porcelain | awk '/^\?\? / && $2 ~ /^research\/.*\.mp3$/ {print $2}')

if [ -z "$UNTRACKED_MP3" ]; then
  echo "No untracked TTS files to commit."
  exit 0
fi

echo "Committing TTS files:"
echo "$UNTRACKED_MP3"

git add $UNTRACKED_MP3
git commit -m "tts: Add audio for newly generated research reports

- Auto‑commit by commit-tts.sh"
echo "Committed $(echo "$UNTRACKED_MP3" | wc -l) file(s)."
