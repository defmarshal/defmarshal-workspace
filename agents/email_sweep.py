#!/usr/bin/env python3
import os, sys, json, subprocess, time

# Config
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1000'))
PAGES_PER_RUN = int(os.getenv('PAGES_PER_RUN', '4'))
API_KEY = os.getenv('MATON_API_KEY')
if not API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
STATE_FILE = '/home/ubuntu/.openclaw/workspace/memory/email-categorizer.state'
LOG_FILE = '/home/ubuntu/.openclaw/workspace/memory/email-categorizer.log'
OPENCLAWS = '/home/ubuntu/.npm-global/bin/openclaw'

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    line = f"[{t}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_state():
    try:
        with open(STATE_FILE) as f:
            exec(compile(f.read(), STATE_FILE, 'exec'), {}, state)
        return state.get('NEXT_PAGE_TOKEN', '')
    except Exception:
        return ''

def save_state(token):
    with open(STATE_FILE, 'w') as f:
        f.write(f"NEXT_PAGE_TOKEN={token}\n")

def categorize(fr, subj):
    lf = fr.lower()
    ls = subj.lower()
    if any(x in lf for x in ['bca', 'bank', 'transaction', 'statement']):
        return 'banking'
    if any(x in ls for x in ['alert', 'error', 'cpu', 'disk', 'monitor']):
        return 'alerts'
    if any(x in ls for x in ['meeting', 'sprint', 'planning', 'standup', 'review']):
        return 'work'
    if any(x in ls for x in ['newsletter', 'digest', 'promo', 'marketing', 'subscribe']):
        return 'newsletters'
    if any(x in lf for x in ['@company.com', '@org', '@work']):
        return 'work'
    if any(x in ls for x in ['timesheet', 'hr', 'payroll', 'leave']):
        return 'hr'
    return 'personal'

def fetch(url):
    cmd = ['curl', '-s', '-f', '-H', f'Authorization: Bearer {API_KEY}', url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def process_batch(page_token):
    url = f"https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults={BATCH_SIZE}"
    if page_token:
        url += f"&pageToken={page_token}"
    log(f"Fetch: {url}")
    resp = fetch(url)
    if resp is None:
        log("curl error")
        return "NO_MORE", None
    try:
        data = json.loads(resp)
        msg_ids = [m['id'] for m in data.get('messages', [])]
        next_token = data.get('nextPageToken', '')
    except Exception as e:
        log(f"JSON parse error: {e}")
        return "NO_MORE", None
    if not msg_ids:
        return "NO_MORE", None
    log(f"Fetched {len(msg_ids)} ids")
    counts = {}
    # Sequential fetch
    for msg_id in msg_ids:
        detail_url = f"https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/{msg_id}?format=full"
        detail = fetch(detail_url)
        if detail is None:
            continue
        try:
            d = json.loads(detail)
            headers = d.get('payload', {}).get('headers', [])
            from_hdr = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
            subj_hdr = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
        except Exception:
            from_hdr = subj_hdr = ''
        cat = categorize(from_hdr, subj_hdr)
        counts[cat] = counts.get(cat, 0) + 1
    total = sum(counts.values())
    for k, v in counts.items():
        log(f"{k}: {v}")
    summary = f"📧 Email batch: {total} unread"
    for k, v in counts.items():
        summary += f"\n  - {k}: {v}"
    print(summary)
    # Send Telegram
    try:
        subprocess.run([OPENCLAWS, 'message', 'send', '--to', 'last', '--text', summary], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        log("Failed to send Telegram")
    return (next_token if next_token else "DONE"), counts

def main():
    log("Starting sweep")
    token = load_state()
    pages = 0
    while pages < PAGES_PER_RUN:
        result, _ = process_batch(token)
        if result in ("NO_MORE", "DONE"):
            token = ''
            break
        else:
            token = result
            pages += 1
    save_state(token or '')
    log(f"Finished: processed {pages} pages. Token: {token or 'none'}")

if __name__ == '__main__':
    main()
