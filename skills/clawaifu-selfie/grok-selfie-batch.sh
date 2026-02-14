#!/bin/bash
# Batch selfie: fetch multiple anime images and send as a zip
# Usage: ./grok-selfie-batch.sh <count> [rating] [caption]
# Example: ./grok-selfie-batch.sh 5 explicit "Here's a set!"

set -euo pipefail

if [ -z "${BOT_TOKEN:-}" ]; then
    echo "Error: BOT_TOKEN environment variable required"
    exit 1
fi

if [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
    echo "Error: TELEGRAM_CHAT_ID environment variable required"
    exit 1
fi

COUNT="${1:-}"
RATING="${2:-safe}"
CAPTION="${3:-}"

if [ -z "$COUNT" ]; then
    echo "Error: count required"
    echo "Usage: $0 <count> [rating] [caption]"
    echo "Example: $0 5 explicit \"Here's a set!\""
    exit 1
fi

if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
    echo "Error: count must be a positive integer"
    exit 1
fi

if [ "$COUNT" -lt 1 ] || [ "$COUNT" -gt 20 ]; then
    echo "Error: count must be between 1 and 20"
    exit 1
fi

if [ "$RATING" != "safe" ] && [ "$RATING" != "explicit" ]; then
    echo "Error: rating must be 'safe' or 'explicit'"
    exit 1
fi

echo "Fetching $COUNT random anime images (rating: $RATING) from Nekos API..."

# Create temp directory for images
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Fetch images
for i in $(seq 1 "$COUNT"); do
  echo "  [$i/$COUNT] Fetching..."
  response=$(curl -s "https://api.nekosapi.com/v4/images/random?rating=$RATING")
  image_url=$(echo "$response" | jq -r '.[0].url')
  
  if [ -z "$image_url" ] || [ "$image_url" = "null" ]; then
    echo "  Warning: failed to get image $i, skipping..."
    continue
  fi
  
  # Download with a unique filename
  ext="${image_url##*.}"
  # If URL has query params, strip them
  ext="${ext%%\?*}"
  # Default to webp if extension is weird
  if [[ "$ext" != "webp" && "$ext" != "jpg" && "$ext" != "jpeg" && "$ext" != "png" ]]; then
    ext="webp"
  fi
  
  tmpfile="$TMPDIR/image_$(printf "%04d" "$i").$ext"
  curl -s -L "$image_url" -o "$tmpfile"
  
  if [ ! -s "$tmpfile" ]; then
    echo "  Warning: downloaded image $i is empty, skipping..."
    rm -f "$tmpfile"
  else
    echo "  ✓ Downloaded image $i"
  fi
done

# Count how many we actually got
downloaded=$(ls -1 "$TMPDIR" | wc -l)
if [ "$downloaded" -eq 0 ]; then
    echo "Error: no images downloaded"
    exit 1
fi

echo "Downloaded $downloaded images. Creating zip archive..."

# Create tar.gz archive (more portable than zip)
ARCHIVE="/tmp/neko_batch_$(date +%s).tar.gz"
tar -czf "$ARCHIVE" -C "$TMPDIR" .

if [ ! -f "$ARCHIVE" ] || [ ! -s "$ARCHIVE" ]; then
    echo "Error: failed to create archive"
    exit 1
fi

echo "Archive created: $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"

# Send to Telegram
CAPTION_TEXT="${CAPTION:-Here are $downloaded anime images from Nekos API! ✨}"
echo "Sending to Telegram..."
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "document=@${ARCHIVE}" \
  -F "caption=${CAPTION_TEXT}" > /dev/null

echo "Done! Batch sent."
rm -f "$ARCHIVE"
