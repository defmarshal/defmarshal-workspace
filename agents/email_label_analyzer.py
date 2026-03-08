#!/usr/bin/env python3
import os, sys, json, subprocess, time, re
from collections import defaultdict

# Config
MATON_API_KEY = os.getenv('MATON_API_KEY')
if not MATON_API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
BASE_URL = "https://gateway.maton.ai/google-mail/gmail/v1/users/me"
STATE_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_analyzer.state'
OUTPUT_FILE = '/home/ubuntu/.openclaw/workspace/memory/label_mapping.json'
LOG_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_analyzer.log'

MAX_UNREAD = int(os.getenv('MAX_UNREAD', '1000'))

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    line = f"[{t}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_processed():
    try:
        with open(STATE_FILE) as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()

def save_processed(ids):
    with open(STATE_FILE, 'w') as f:
        for i in ids:
            f.write(f"{i}\n")

def curl_get(url):
    cmd = ['curl', '-s', '-f', '-H', f'Authorization: Bearer {MATON_API_KEY}', url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    return res.stdout

def fetch_unread_ids(limit=1000):
    ids = []
    page_token = None
    while len(ids) < limit:
        url = f"{BASE_URL}/messages?q=is:unread&maxResults=100"
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
    # Gmail label name restrictions: no control chars, no leading/trailing spaces, max 255
    # Replace problematic chars with hyphen, collapse spaces
    name = name.strip()
    # Remove slashes and quotes
    name = re.sub(r'[/"]', '-', name)
    # Replace other problematic chars with hyphen
    name = re.sub(r'[\\\[\]<>\(\)\.\,\:\;\=\>\<\?\!\@\#\$\%\^\&\*\+\|]', '-', name)
    # Collapse multiple hyphens/spaces
    name = re.sub(r'[\s-]+', '-', name)
    return name[:50] or 'Unknown'

def analyze_emails():
    processed = load_processed()
    ids = fetch_unread_ids(MAX_UNREAD)
    new_ids = [i for i in ids if i not in processed]
    log(f"Total unread: {len(ids)}; new to analyze: {len(new_ids)}")
    if not new_ids:
        log("Nothing new to analyze")
        return {}
    # Build distinct senders map: sender_key (name+email) -> set of domains
    senders = defaultdict(set)
    for i, msg_id in enumerate(new_ids, 1):
        msg = fetch_message(msg_id)
        if not msg:
            continue
        from_hdr = get_header(msg, 'From')
        subject_hdr = get_header(msg, 'Subject')
        name, domain = parse_email_address(from_hdr)
        # Use combined key: "Name <domain>" if name, else just domain
        key = f"{name} <{domain}>" if name else domain
        senders[key].add(domain)
        processed.add(msg_id)
        if i % 10 == 0:
            log(f"Processed {i}/{len(new_ids)}")
            time.sleep(0.2)
    # Build label mapping: for each sender, create a Sweep/... label
    label_mapping = {}
    for sender_key in senders.keys():
        # Derive a nice label name from sender. Prefer name part, fallback to domain.
        if '<' in sender_key:
            name_part = sender_key.split('<')[0].strip()
            # Clean name for label
            label_name = f"Sweep/{sanitize_label(name_part)}"
        else:
            # domain only
            label_name = f"Sweep/{sanitize_label(sender_key)}"
        label_mapping[sender_key] = label_name
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(label_mapping, f, indent=2)
    save_processed(processed)
    log(f"Analysis complete: {len(processed)} total processed, {len(label_mapping)} distinct senders mapped. Saved to {OUTPUT_FILE}")
    # Print summary
    print("\n=== Label Mapping Summary ===")
    counts = defaultdict(int)
    for lbl in label_mapping.values():
        counts[lbl] += 1
    for lbl, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{lbl}: {cnt} sender(s)")
    return label_mapping

if __name__ == '__main__':
    analyze_emails()
