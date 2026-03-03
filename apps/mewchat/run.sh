#!/usr/bin/env bash
# MewChat — standalone chat with mewmew
# Serves the MewChat PWA on port 3002 (default)

PORT=${1:-3002}
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🐾 Starting MewChat on http://0.0.0.0:$PORT"
echo "Press Ctrl+C to stop."
echo ""
echo "Note: Make sure MewDash backend is running on http://localhost:3001"
echo "      or edit config.js to set the correct API_BASE."
echo ""

cd "$DIR"
exec python3 -m http.server --bind 0.0.0.0 $PORT