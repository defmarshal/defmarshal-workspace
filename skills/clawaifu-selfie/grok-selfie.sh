#!/bin/bash
# clawaifu-selfie - Send random anime images from Nekos API
# Free, no API key required, curated collection of 40k+ anime images
# Ratings: safe (default) or explicit (NSFW)

set -euo pipefail

if [ -z "${BOT_TOKEN:-}" ]; then
    echo "Error: BOT_TOKEN environment variable required"
    exit 1
fi

if [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
    echo "Error: TELEGRAM_CHAT_ID environment variable required"
    exit 1
fi

CAPTION="${1:-Random anime from Nekos API! ✨}"
RATING="${2:-safe}"  # safe (default) or explicit

if [ "$RATING" != "safe" ] && [ "$RATING" != "explicit" ]; then
    echo "Error: Rating must be 'safe' or 'explicit'"
    exit 1
fi

echo "Fetching random anime image from Nekos API (rating: $RATING)..."

# Get the API response (array of images) with rating filter
response=$(curl -s "https://api.nekosapi.com/v4/images/random?rating=$RATING")

# Extract the first image URL using jq
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required to parse JSON"
    exit 1
fi

image_url=$(echo "$response" | jq -r '.[0].url')

if [ -z "$image_url" ] || [ "$image_url" = "null" ]; then
    echo "Error: No image URL in response"
    echo "Response: $response"
    exit 1
fi

echo "Image URL: $image_url"

# Download the image
tmpfile="/tmp/neko_selfie_$(date +%s).webp"
curl -s -L "$image_url" -o "$tmpfile"

if [ ! -s "$tmpfile" ]; then
    echo "Error: Downloaded image is empty"
    exit 1
fi

echo "Image downloaded to $tmpfile"

# Send to Telegram with caption
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@${tmpfile};type=image/webp" \
  -F "caption=${CAPTION}" > /dev/null

echo "Done! Selfie sent."
rm -f "$tmpfile"
