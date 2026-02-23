#!/usr/bin/env bash
# Check if Research Hub needs redeployment by comparing research/ and public/research

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
PUBLIC_DIR="$WORKSPACE/apps/research-hub/public/research"

echo "Research Hub sync check"
echo "----------------------"

if [ ! -d "$PUBLIC_DIR" ]; then
  echo "Public directory missing! Run deploy-research-hub.sh"
  exit 1
fi

# Count files
total_md=$(ls -1 "$RESEARCH_DIR"/*.md 2>/dev/null | wc -l)
public_md=$(ls -1 "$PUBLIC_DIR"/*.md 2>/dev/null | wc -l)

total_mp3=$(ls -1 "$RESEARCH_DIR"/*.mp3 2>/dev/null | wc -l)
public_mp3=$(ls -1 "$PUBLIC_DIR"/*.mp3 2>/dev/null | wc -l)

echo "Markdown: $public_md / $total_md in sync"
echo "MP3:     $public_mp3 / $total_mp3 in sync"

if [ $public_md -eq $total_md ] && [ $public_mp3 -eq $total_mp3 ]; then
  echo "✅ Research Hub is up to date"
  exit 0
else
  echo "⚠️  Research Hub is outdated. Run: ./quick deploy-hub"
  exit 1
fi
