#!/usr/bin/env bash
# youtube-digest.sh — Daily YouTube subscription digest
#
# Fetches your YouTube subscriptions, checks for new uploads in the last 24h,
# summarizes video content (transcript or description), and sends a digest to Telegram.
#
# Prerequisites: run scripts/youtube-oauth-setup.sh first.
# Usage: ./scripts/youtube-digest.sh [--hours N] [--dry-run]

set -euo pipefail

WORKSPACE="${WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CREDS_FILE="$WORKSPACE/config/youtube-credentials.json"
CONTENT_DIR="$WORKSPACE/content"
TELEGRAM_SESSION_ID="bcc62cdd-c612-4f74-8f20-559e10b3dad6"
LOG="$WORKSPACE/memory/youtube-digest.log"
HOURS=24
DRY_RUN=0

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --hours) HOURS="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) shift ;;
  esac
done

log() { echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $*" | tee -a "$LOG"; }
log_err() { echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ERROR: $*" | tee -a "$LOG" >&2; }

log "=== YouTube Digest starting (hours=$HOURS, dry_run=$DRY_RUN) ==="

# ── Check credentials ──────────────────────────────────────────────────────
if [ ! -f "$CREDS_FILE" ]; then
  log_err "Credentials not found: $CREDS_FILE"
  log_err "Run ./scripts/youtube-oauth-setup.sh first"
  exit 1
fi

# ── Token management (Python) ──────────────────────────────────────────────
python3 - <<'PYEOF' || { log_err "Token refresh failed"; exit 1; }
import json, urllib.request, urllib.parse, os, sys, time

creds_file = os.environ.get('CREDS_FILE', '')
with open(creds_file) as f:
    creds = json.load(f)

def refresh_token(creds):
    data = urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token',
    }).encode()
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token', data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())
    creds['access_token'] = resp['access_token']
    if 'refresh_token' in resp:
        creds['refresh_token'] = resp['refresh_token']
    with open(creds_file, 'w') as f:
        json.dump(creds, f, indent=2)
    print('Token refreshed')

# Always refresh to ensure it's valid
try:
    refresh_token(creds)
except Exception as e:
    print(f'Refresh warning: {e}', file=sys.stderr)
    # Try using existing token anyway
PYEOF

export CREDS_FILE

# ── Main digest logic (Python) ─────────────────────────────────────────────
DIGEST=$(python3 - <<PYEOF
import json, urllib.request, sys, os, subprocess, time
from datetime import datetime, timezone, timedelta

creds_file = os.environ.get('CREDS_FILE', '')
hours = int(os.environ.get('HOURS', '24'))
workspace = os.environ.get('WORKSPACE', '')

with open(creds_file) as f:
    creds = json.load(f)

access_token = creds['access_token']

def yt_get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f'HTTP {e.code} for {url}: {err_body[:200]}', file=sys.stderr)
        return None
    except Exception as e:
        print(f'Error fetching {url}: {e}', file=sys.stderr)
        return None

# Cutoff time
cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
cutoff_str = cutoff.isoformat()

print(f'Fetching subscriptions...', file=sys.stderr)

# Fetch subscriptions (paginate)
subs = []
next_page = ''
page = 0
while page < 5:  # max 250 subs (5 pages * 50)
    url = f'https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&maxResults=50&order=alphabetical'
    if next_page:
        url += f'&pageToken={next_page}'
    data = yt_get(url)
    if not data:
        break
    items = data.get('items', [])
    for item in items:
        snip = item.get('snippet', {})
        channel_id = snip.get('resourceId', {}).get('channelId', '')
        channel_title = snip.get('title', 'Unknown')
        if channel_id:
            subs.append({'id': channel_id, 'title': channel_title})
    next_page = data.get('nextPageToken', '')
    page += 1
    if not next_page:
        break

print(f'Found {len(subs)} subscriptions', file=sys.stderr)

if not subs:
    print('No subscriptions found.', file=sys.stderr)
    print('NO_SUBS')
    sys.exit(0)

# For each subscription, get uploads playlist and check for recent videos
new_videos = []

def get_uploads_playlist(channel_id):
    # Channel's uploads playlist ID = UC... -> UU...
    return 'UU' + channel_id[2:]

def get_recent_uploads(channel_id, channel_title):
    playlist_id = get_uploads_playlist(channel_id)
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={playlist_id}&maxResults=5'
    data = yt_get(url)
    if not data:
        return []
    videos = []
    for item in data.get('items', []):
        snip = item.get('snippet', {})
        pub_at = snip.get('publishedAt', '')
        if not pub_at:
            continue
        # Parse publish time
        try:
            pub_dt = datetime.fromisoformat(pub_at.replace('Z', '+00:00'))
        except:
            continue
        if pub_dt < cutoff:
            break  # sorted newest first
        vid_id = snip.get('resourceId', {}).get('videoId', '') or item.get('contentDetails', {}).get('videoId', '')
        if not vid_id:
            continue
        title = snip.get('title', 'Untitled')
        desc = snip.get('description', '')[:500]
        videos.append({
            'id': vid_id,
            'title': title,
            'description': desc,
            'channel': channel_title,
            'published_at': pub_at,
            'url': f'https://youtube.com/watch?v={vid_id}',
        })
    return videos

# Process subscriptions (limit to avoid rate limits)
processed = 0
for sub in subs:
    try:
        videos = get_recent_uploads(sub['id'], sub['title'])
        new_videos.extend(videos)
        processed += 1
        if processed % 10 == 0:
            print(f'Processed {processed}/{len(subs)} channels, found {len(new_videos)} new videos...', file=sys.stderr)
        # Small delay to avoid rate limits
        time.sleep(0.05)
    except Exception as e:
        print(f'Error for {sub["title"]}: {e}', file=sys.stderr)

print(f'Total new videos in last {hours}h: {len(new_videos)}', file=sys.stderr)

if not new_videos:
    print(f'NO_NEW_VIDEOS:{hours}h')
    sys.exit(0)

# Try to get transcripts for each video
def get_transcript(video_id, max_words=200):
    try:
        result = subprocess.run(
            ['python3', '-c',
             f'from youtube_transcript_api import YouTubeTranscriptApi; '
             f't=YouTubeTranscriptApi.get_transcript("{video_id}"); '
             f'print(" ".join([x["text"] for x in t[:60]]))'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            words = result.stdout.strip().split()
            return ' '.join(words[:max_words])
    except Exception:
        pass
    return ''

# Get video details (duration, view count) in batch
def get_video_details(video_ids):
    ids_str = ','.join(video_ids[:50])
    url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={ids_str}'
    data = yt_get(url)
    if not data:
        return {}
    result = {}
    for item in data.get('items', []):
        vid_id = item['id']
        duration = item.get('contentDetails', {}).get('duration', '')
        views = item.get('statistics', {}).get('viewCount', '')
        # Parse ISO 8601 duration PT1H2M3S
        import re
        dur_match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if dur_match:
            h = int(dur_match.group(1) or 0)
            m = int(dur_match.group(2) or 0)
            s = int(dur_match.group(3) or 0)
            total_min = h * 60 + m + (1 if s >= 30 else 0)
            dur_str = f'{h}h{m:02d}m' if h > 0 else f'{m}m{s:02d}s'
        else:
            dur_str = ''
        result[vid_id] = {'duration': dur_str, 'views': views}
    return result

# Batch video details
video_ids = [v['id'] for v in new_videos]
video_details = get_video_details(video_ids)

# Try to install youtube-transcript-api if not available
try:
    import youtube_transcript_api
    has_transcript_api = True
except ImportError:
    try:
        subprocess.run(['pip3', 'install', 'youtube-transcript-api', '-q'], check=True, timeout=30)
        has_transcript_api = True
    except:
        has_transcript_api = False

# Build digest markdown
date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
time_str = datetime.now(timezone.utc).strftime('%H%M')

lines = [
    f'# 📺 YouTube Digest — {date_str}',
    f'> New uploads from your subscriptions in the last {hours}h',
    f'> {len(new_videos)} video(s) from {len(set(v["channel"] for v in new_videos))} channel(s)',
    '',
]

# Group by channel
from collections import defaultdict
by_channel = defaultdict(list)
for v in new_videos:
    by_channel[v['channel']].append(v)

for channel, videos in sorted(by_channel.items()):
    lines.append(f'## 📡 {channel}')
    lines.append('')
    for v in videos:
        details = video_details.get(v['id'], {})
        dur = details.get('duration', '')
        views = details.get('views', '')
        views_fmt = f'{int(views):,}' if views else ''

        pub_dt = datetime.fromisoformat(v['published_at'].replace('Z', '+00:00'))
        pub_str = pub_dt.strftime('%b %d, %H:%M UTC')

        lines.append(f'### [{v["title"]}]({v["url"]})')
        meta_parts = [f'📅 {pub_str}']
        if dur: meta_parts.append(f'⏱ {dur}')
        if views_fmt: meta_parts.append(f'👁 {views_fmt} views')
        lines.append(' · '.join(meta_parts))
        lines.append('')

        # Get content for summary
        content = ''
        if has_transcript_api:
            content = get_transcript(v['id'])
        if not content and v['description']:
            content = v['description'][:400]

        if content:
            lines.append(f'**Content preview:** {content[:300]}...' if len(content) > 300 else f'**Content preview:** {content}')
            lines.append('')

    lines.append('')

lines.append(f'---')
lines.append(f'*Generated by youtube-digest.sh at {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}*')

digest_md = '\n'.join(lines)
print(digest_md)
PYEOF
)

export HOURS

# Check for special outputs
if echo "$DIGEST" | grep -q "^NO_SUBS"; then
  log "No YouTube subscriptions found. Check OAuth credentials."
  exit 0
fi

if echo "$DIGEST" | grep -qE "^NO_NEW_VIDEOS:"; then
  HOURS_OUT=$(echo "$DIGEST" | grep -oE '[0-9]+h')
  log "No new videos in the last $HOURS_OUT. Nothing to digest."
  [ "$DRY_RUN" -eq 1 ] && echo "Dry run: nothing to send."
  exit 0
fi

# Save digest to content/
mkdir -p "$CONTENT_DIR"
DATE_STR=$(date -u '+%Y-%m-%d')
TIME_STR=$(date -u '+%H%M')
OUTPUT_FILE="$CONTENT_DIR/youtube-digest-${DATE_STR}-${TIME_STR}.md"
echo "$DIGEST" > "$OUTPUT_FILE"
log "Digest saved: $OUTPUT_FILE"

# ── Send to Telegram ──────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
  log "Dry run: skipping Telegram delivery"
  echo "--- DIGEST PREVIEW ---"
  echo "$DIGEST" | head -40
  exit 0
fi

# Build compact Telegram message (Telegram has 4096 char limit)
TELEGRAM_MSG=$(python3 - <<TMSG
import sys, os
digest = """$DIGEST"""

lines = digest.split('\n')
tg_lines = []
for line in lines:
    if line.startswith('**Content preview:**'):
        # Shorten content preview
        line = line[:120] + '...' if len(line) > 120 else line
    tg_lines.append(line)

msg = '\n'.join(tg_lines)
# Truncate to Telegram limit
if len(msg) > 3800:
    msg = msg[:3800] + '\n\n…[see content/youtube-digest.md for full digest]'
print(msg)
TMSG
)

log "Sending digest to Telegram..."
openclaw agent \
  --session-id "$TELEGRAM_SESSION_ID" \
  --message "$TELEGRAM_MSG" \
  --deliver \
  2>>"$LOG" && log "Digest delivered to Telegram" || log "WARNING: Telegram delivery failed"

log "=== YouTube Digest complete ==="
