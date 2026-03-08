#!/usr/bin/env python3
import os, sys, json, subprocess, time, re
from collections import defaultdict

# Config
MATON_API_KEY = os.getenv('MATON_API_KEY')
if not MATON_API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
BASE_URL = "https://gateway.maton.ai/google-mail/gmail/v1/users/me"
OUTPUT_FILE = '/home/ubuntu/.openclaw/workspace/memory/label_mapping_1000.json'
LOG_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_analyzer_1000.log'

MAX_MESSAGES = 1000

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    line = f"[{t}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def curl_get(url):
    cmd = ['curl', '-s', '-f', '-H', f'Authorization: Bearer {MATON_API_KEY}', url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    return res.stdout

def fetch_recent_ids(limit=1000):
    ids = []
    page_token = None
    while len(ids) < limit:
        url = f"{BASE_URL}/messages?maxResults=100"
        if page_token:
            url += f"&pageToken={page_token}"
        resp = curl_get(url)
        if not resp:
            break
        try:
            data = json.loads(resp)
            batch = [m['id'] for m in data.get('messages', [])]
            ids.extend(batch)
            if len(ids) >= limit:
                ids = ids[:limit]
                break
            page_token = data.get('nextPageToken')
            if not page_token:
                break
        except Exception as e:
            log(f"JSON error: {e}")
            break
    return ids

def fetch_message(msg_id):
    url = f"{BASE_URL}/messages/{msg_id}?format=full"
    resp = curl_get(url)
    if not resp:
        return None
    try:
        return json.loads(resp)
    except Exception:
        return None

def get_header(msg, name):
    headers = msg.get('payload', {}).get('headers', [])
    for h in headers:
        if h.get('name', '').lower() == name.lower():
            return h.get('value', '')
    return ''

def parse_email_address(addr: str):
    if '<' in addr and '>' in addr:
        name_part = addr.split('<')[0].strip()
        email_part = addr.split('<')[1].split('>')[0].strip()
    else:
        name_part = ''
        email_part = addr.strip()
    if '@' in email_part:
        local, domain = email_part.split('@', 1)
    else:
        local, domain = email_part, ''
    return name_part, domain

def sanitize_label(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[/"]', '-', name)
    name = re.sub(r'[\\\[\]<>\(\)\.\,\:\;\=\>\<\?\!\@\#\$\%\^\&\*\+\|]', '-', name)
    name = re.sub(r'[\s-]+', '-', name)
    return name[:50] or 'Unknown'

def analyze_emails():
    log(f"Fetching up to {MAX_MESSAGES} recent messages...")
    ids = fetch_recent_ids(MAX_MESSAGES)
    log(f"Fetched {len(ids)} message IDs")
    senders = {}
    for i, msg_id in enumerate(ids, 1):
        msg = fetch_message(msg_id)
        if not msg:
            continue
        from_hdr = get_header(msg, 'From')
        name, domain = parse_email_address(from_hdr)
        key = f"{name} <{domain}>" if name else domain
        if key not in senders:
            # Derive label name
            if name:
                label_name = f"Sweep/{sanitize_label(name)}"
            elif domain:
                label_name = f"Sweep/{sanitize_label(domain)}"
            else:
                label_name = "Sweep/Unknown"
            senders[key] = label_name
        if i % 50 == 0:
            log(f"Processed {i}/{len(ids)}")
            time.sleep(0.1)
    # Save mapping
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(senders, f, indent=2)
    log(f"Analysis complete: {len(senders)} distinct senders mapped. Saved to {OUTPUT_FILE}")
    # Print summary
    print("\n=== Label Mapping Summary (top 20) ===")
    counts = defaultdict(int)
    for lbl in senders.values():
        counts[lbl] += 1
    for lbl, cnt in sorted(counts.items(), key=lambda x: -x[1])[:20]:
        print(f"{lbl}: {cnt} sender(s)")
    return senders

if __name__ == '__main__':
    analyze_emails()
