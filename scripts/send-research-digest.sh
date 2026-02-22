#!/usr/bin/env bash
# Send daily research digest via Gmail (using Maton API)
# Requires MATON_API_KEY in env or ~/.openclaw/openclaw.json

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
STATE_FILE="$WORKSPACE/.last_digest_sent"
LOG_FILE="$WORKSPACE/logs/digest.log"

# Configuration
TO_EMAIL="${DIGEST_TO_EMAIL:-}"  # recipient email
FROM_NAME="Research Agent"
SUBJECT="Research Digest — $(date -u +%Y-%m-%d)"

# Load MATON_API_KEY from openclaw.json if not in env
if [ -z "${MATON_API_KEY:-}" ]; then
  if [ -f "$HOME/.openclaw/openclaw.json" ]; then
    MATON_API_KEY=$(grep -o '"MATON_API_KEY":"[^"]*"' "$HOME/.openclaw/openclaw.json" | cut -d'"' -f4 || true)
  fi
fi

if [ -z "${MATON_API_KEY:-}" ]; then
  echo "Error: MATON_API_KEY not set" >&2
  exit 1
fi

if [ -z "$TO_EMAIL" ]; then
  echo "Error: DIGEST_TO_EMAIL not set" >&2
  exit 1
fi

# Determine reports since last digest
last_slug=""
if [ -f "$STATE_FILE" ]; then
  last_slug=$(cat "$STATE_FILE" | tr -d '\n')
fi

echo "=== Digest $(date -u) ===" >> "$LOG_FILE"
echo "Last slug: ${last_slug:-none}" >> "$LOG_FILE"

# Collect new reports
reports=()
shopt -s nullglob
for md in "$RESEARCH_DIR"/*.md; do
  slug=$(basename "$md" .md)
  if [ -n "$last_slug" ]; then
    # Compare by filename lexicographic (works if YYYY-MM-DD prefix)
    if [[ "$slug" < "$last_slug" ]]; then
      continue
    fi
  fi
  reports+=("$md")
done

# If no new reports, exit
if [ ${#reports[@]} -eq 0 ]; then
  echo "No new reports since $last_slug" >> "$LOG_FILE"
  exit 0
fi

echo "New reports: ${#reports[@]}" >> "$LOG_FILE"

# Build HTML email content
HTML="<html><body>"
HTML+="<h2>Latest Research Reports</h2>"
HTML+="<ul>"
for md in "${reports[@]}"; do
  slug=$(basename "$md" .md)
  title=$(grep -m1 '^title:' "$md" | sed 's/^title:[[:space:]]*//' | tr -d '"' || true)
  if [ -z "$title" ]; then
    title="$slug"
  fi
  audio=""
  if [ -f "$RESEARCH_DIR/$slug.mp3" ]; then
    audio=" 🎧"
  fi
  HTML+="<li><a href=\"https://research-hub-flame.vercel.app/research/$slug\">$title</a>$audio</li>"
done
HTML+="</ul>"
HTML+="<p><small>Sent by your friendly research agent.</small></p>"
HTML+="</body></html>"

# Send via Maton API (Gmail)
API_URL="https://api.maton.is/v1/send"
JSON="{\"to\":\"$TO_EMAIL\",\"subject\":\"$SUBJECT\",\"html\":\"$HTML\"}"

echo "Sending email to $TO_EMAIL..." >> "$LOG_FILE"
curl -s -X POST "$API_URL" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON" >> "$LOG_FILE" 2>&1

# Update state file to the newest slug
newest="${reports[-1]}"
newest_slug=$(basename "$newest" .md)
echo "$newest_slug" > "$STATE_FILE"
echo "Digest sent; state updated to $newest_slug" >> "$LOG_FILE"

echo "✅ Digest sent" >&2
