#!/bin/bash
# clawaifu-selfie - Generate anime selfies using Craiyon.com (free, no key)
# Security: credentials via environment only

set -euo pipefail

if [ -z "${BOT_TOKEN:-}" ]; then
    echo "Error: BOT_TOKEN environment variable required"
    exit 1
fi

TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

if [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "Error: TELEGRAM_CHAT_ID environment variable required"
    exit 1
fi

USER_CONTEXT="${1:-}"
MODE="${2:-mirror}"
CAPTION="${3:-}"

if [ -z "$USER_CONTEXT" ]; then
    echo "Usage: $0 <user_context> [mirror|direct] [caption]"
    exit 1
fi

CHARACTER="Reze from Chainsaw Man"
STYLE="anime style, 2D animation, cel shading, vibrant colors"
FACE="green eyes, thin line mouth, subtle smile with closed lips, black choker"
OUTFIT="wearing outfit appropriate for the situation, black choker always visible"

if [ "$MODE" == "direct" ]; then
    PROMPT="$CHARACTER, $STYLE, $FACE, $OUTFIT, close-up portrait selfie at $USER_CONTEXT, direct eye contact, cinematic lighting, high detail, sharp focus"
else
    PROMPT="$CHARACTER, $STYLE, $FACE, $OUTFIT, mirror selfie full-body shot, $USER_CONTEXT, casual pose, looking at camera"
fi

echo "Generating image via Craiyon..."
RESPONSE=$(curl -s -X POST "https://www.craiyon.com/v1/models" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"$PROMPT\",\"num_images\":1,\"size\":256}")

IMAGE_BASE64=$(echo "$RESPONSE" | jq -r '.images[0] // empty')

if [ -z "$IMAGE_BASE64" ]; then
    echo "Error: No image returned"
    echo "Response: $RESPONSE"
    exit 1
fi

IMAGE_TMP="/tmp/selfie_$$.jpg"
echo "$IMAGE_BASE64" | base64 -d > "$IMAGE_TMP" 2>/dev/null || {
    python3 -c "import base64, sys; sys.stdout.buffer.write(base64.b64decode('''$IMAGE_BASE64'''))" > "$IMAGE_TMP"
}

if [ -n "$CAPTION" ]; then
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendPhoto" \
      -F "chat_id=$TELEGRAM_CHAT_ID" \
      -F "photo=@$IMAGE_TMP;type=image/jpeg" \
      -F "caption=$CAPTION" > /dev/null 2>&1
else
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendPhoto" \
      -F "chat_id=$TELEGRAM_CHAT_ID" \
      -F "photo=@$IMAGE_TMP;type=image/jpeg" > /dev/null 2>&1
fi

rm -f "$IMAGE_TMP"
echo "Done! Selfie sent via Craiyon."
