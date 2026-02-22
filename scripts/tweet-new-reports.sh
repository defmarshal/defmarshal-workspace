#!/usr/bin/env bash
# Auto‑tweet new research reports
# Requires Twitter API credentials in environment: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
# Optional: --dry-run, --since <timestamp_file>

set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
RESEARCH_DIR="$WORKSPACE/research"
STATE_FILE="$WORKSPACE/.last_tweeted"
DRY_RUN=0
SINCE_FILE=""

usage() {
  echo "Usage: $0 [--dry-run] [--since <timestamp_file>]" >&2
  echo "  --dry-run    Print tweets without posting" >&2
  echo "  --since      File containing last tweeted report slug (default: $STATE_FILE)" >&2
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --since) SINCE_FILE="$2"; shift 2 ;;
    *) usage ;;
  esac
done

SINCE_FILE="${SINCE_FILE:-$STATE_FILE}"

# Check credentials
if [ -z "${TWITTER_API_KEY:-}" ] || [ -z "${TWITTER_ACCESS_TOKEN:-}" ]; then
  echo "Error: Twitter API credentials not set in environment." >&2
  echo "Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET" >&2
  exit 1
fi

# Determine last tweeted slug
last_slug=""
if [ -f "$SINCE_FILE" ]; then
  last_slug=$(cat "$SINCE_FILE" | tr -d '\n')
fi

echo "Last tweeted slug: ${last_slug:-none}"

# Find new reports (sorted by date from filename)
shopt -s nullglob
new_reports=()
for md in "$RESEARCH_DIR"/*.md; do
  slug=$(basename "$md" .md)
  # If state file exists, skip until we find the last one, then mark subsequent as new
  if [ -n "$last_slug" ]; then
    if [ "$slug" = "$last_slug" ]; then
      last_slug=""  # Found the last; subsequent will be new
      continue
    fi
    if [ -n "$last_slug" ]; then
      continue  # still before last_slug
    fi
  fi
  new_reports+=("$md")
done

if [ ${#new_reports[@]} -eq 0 ]; then
  echo "No new reports to tweet."
  exit 0
fi

echo "New reports to tweet: ${#new_reports[@]}"

# Twitter API v2 endpoints (OAuth 1.0a required)
# We'll use twurl if available, else fallback to curl with oauth signing via oauth1.0a tool (not installed). For now, outline twurl approach.

# Install twurl if not present: gem install twurl
if ! command -v twurl &>/dev/null; then
  echo "twurl not found. Install with: gem install twurl" >&2
  echo "Then configure: twurl configure --consumer-key $TWITTER_API_KEY --consumer-secret $TWITTER_API_SECRET" >&2
  exit 1
fi

# Configure twurl with access token if not already
# We can set via env: TWURL_ACCESS_TOKEN, TWURL_ACCESS_TOKEN_SECRET? Actually twurl stores in ~/.twurlrc; we can pass via header manually but twurl handles.

# Compose and tweet each report
for md in "${new_reports[@]}"; do
  slug=$(basename "$md" .md)
  # Extract title from frontmatter or filename
  title=$(grep -m1 '^title:' "$md" | sed 's/^title:[[:space:]]*//' | tr -d '"' || true)
  if [ -z "$title" ]; then
    title=$(echo "$slug" | sed 's/^2026-02-//; s/-/ /g')
  fi

  # Build tweet: title + short link + optional audio mention
  tweet="$title — research.defmarshal.com/research/$slug"
  if [ -f "$RESEARCH_DIR/$slug.mp3" ]; then
    tweet="$tweet (with audio)"
  fi
  # Truncate to 280 chars
  tweet=$(echo "$tweet" | head -c 280)

  echo "Would tweet: $tweet"

  if [ $DRY_RUN -eq 0 ]; then
    # Post via Twitter API
    twurl -d "text=$tweet" /2/tweets.json || { echo "Tweet failed for $slug"; exit 1; }
    # Update state file to this slug
    echo "$slug" > "$STATE_FILE"
  fi
done

echo "Done."
