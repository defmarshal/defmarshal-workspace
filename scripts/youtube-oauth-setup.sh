#!/usr/bin/env bash
# youtube-oauth-setup.sh — Interactive YouTube Data API v3 OAuth setup
# Saves credentials to config/youtube-credentials.json
#
# Prerequisites:
#   1. Go to https://console.cloud.google.com
#   2. Create or select a project
#   3. Enable "YouTube Data API v3" (APIs & Services → Library)
#   4. Create OAuth 2.0 credentials:
#      - Credentials → Create credentials → OAuth client ID
#      - Application type: Desktop app
#      - Download or copy client_id and client_secret
#   5. Run this script

set -euo pipefail

WORKSPACE="${WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CREDS_FILE="$WORKSPACE/config/youtube-credentials.json"
SCOPE="https://www.googleapis.com/auth/youtube.readonly"
REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob"

# Colors
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   YouTube OAuth Setup — subscription digest  ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Prerequisites:${NC}"
echo "  1. Google Cloud project with YouTube Data API v3 enabled"
echo "  2. OAuth 2.0 credentials (Desktop app type)"
echo "  See: https://console.cloud.google.com/apis/credentials"
echo ""

# Check if already configured
if [ -f "$CREDS_FILE" ]; then
  refresh_token=$(python3 -c "import json; d=json.load(open('$CREDS_FILE')); print(d.get('refresh_token',''))" 2>/dev/null || echo "")
  if [ -n "$refresh_token" ]; then
    echo -e "${GREEN}✓ Credentials already configured at:${NC} $CREDS_FILE"
    echo ""
    read -rp "Re-run OAuth setup? [y/N] " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
      echo "Skipping — existing credentials kept."
      exit 0
    fi
  fi
fi

# Prompt for client credentials
echo -e "${YELLOW}Step 1: Enter your OAuth 2.0 client credentials${NC}"
echo "(From Google Cloud Console → Credentials → your OAuth client)"
echo ""
read -rp "Client ID:     " CLIENT_ID
read -rp "Client Secret: " CLIENT_SECRET

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
  echo -e "${RED}Error: client_id and client_secret are required.${NC}"
  exit 1
fi

# Build OAuth URL
AUTH_URL="https://accounts.google.com/o/oauth2/v2/auth?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${SCOPE}&access_type=offline&prompt=consent"

echo ""
echo -e "${YELLOW}Step 2: Authorize the application${NC}"
echo ""
echo -e "${CYAN}Open this URL in your browser:${NC}"
echo ""
echo "$AUTH_URL"
echo ""
echo -e "${YELLOW}Sign in with your Google account, authorize the app, then copy the authorization code.${NC}"
echo ""
read -rp "Authorization code: " AUTH_CODE

if [ -z "$AUTH_CODE" ]; then
  echo -e "${RED}Error: authorization code is required.${NC}"
  exit 1
fi

echo ""
echo -e "${YELLOW}Step 3: Exchanging authorization code for tokens…${NC}"

# Exchange code for tokens
TOKEN_RESPONSE=$(python3 - <<PYEOF
import urllib.request, urllib.parse, json, sys

data = urllib.parse.urlencode({
    'client_id': '${CLIENT_ID}',
    'client_secret': '${CLIENT_SECRET}',
    'code': '${AUTH_CODE}',
    'grant_type': 'authorization_code',
    'redirect_uri': '${REDIRECT_URI}',
}).encode()

req = urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())
        print(json.dumps(resp))
except urllib.error.HTTPError as e:
    err = json.loads(e.read())
    print(json.dumps({'error': err.get('error','http_error'), 'error_description': err.get('error_description', str(e))}))
except Exception as e:
    print(json.dumps({'error': 'exception', 'error_description': str(e)}))
PYEOF
)

# Check for error
ERROR=$(python3 -c "import json; d=json.loads('$TOKEN_RESPONSE'); print(d.get('error',''))" 2>/dev/null || echo "parse_error")
if [ -n "$ERROR" ]; then
  ERROR_DESC=$(python3 -c "import json; d=json.loads('$TOKEN_RESPONSE'); print(d.get('error_description',''))" 2>/dev/null || echo "")
  echo -e "${RED}✗ Token exchange failed: $ERROR${NC}"
  [ -n "$ERROR_DESC" ] && echo "  $ERROR_DESC"
  exit 1
fi

# Save credentials
mkdir -p "$(dirname "$CREDS_FILE")"
python3 - <<PYEOF
import json

tokens = json.loads('$TOKEN_RESPONSE')
creds = {
    'client_id': '${CLIENT_ID}',
    'client_secret': '${CLIENT_SECRET}',
    'access_token': tokens.get('access_token', ''),
    'refresh_token': tokens.get('refresh_token', ''),
    'token_type': tokens.get('token_type', 'Bearer'),
    'expires_in': tokens.get('expires_in', 3600),
    'scope': '${SCOPE}',
}
with open('${CREDS_FILE}', 'w') as f:
    json.dump(creds, f, indent=2)
print('Credentials saved successfully.')
PYEOF

echo ""
echo -e "${GREEN}✓ OAuth setup complete!${NC}"
echo -e "  Credentials saved to: ${CYAN}$CREDS_FILE${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  • Run a test digest: ./scripts/youtube-digest.sh"
echo "  • The daily digest cron job runs at 09:00 Asia/Bangkok"
echo ""
echo -e "${CYAN}Note:${NC} credentials are gitignored — do not commit them."
