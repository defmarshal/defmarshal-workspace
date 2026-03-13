#!/usr/bin/env python3
import os, sys, json, subprocess, time, re

# Load .env file if present
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, _, value = line.partition('=')
                os.environ[key.strip()] = value.strip()

# Config
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1000'))
PAGES_PER_RUN = int(os.getenv('PAGES_PER_RUN', '4'))
API_KEY = os.getenv('MATON_API_KEY')
if not API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
STATE_FILE = '/home/ubuntu/.openclaw/workspace/memory/email-categorizer.state'
LOG_FILE = '/home/ubuntu/.openclaw/workspace/memory/email-categorizer.log'
LABEL_MAP_FILE = '/home/ubuntu/.openclaw/workspace/memory/label_mapping.json'
LABEL_CACHE_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_labels.json'
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

def load_sender_mapping():
    try:
        with open(LABEL_MAP_FILE) as f:
            data = json.load(f)
        return data  # dict: "Sender <domain>" -> "Sweep/Name"
    except Exception:
        return {}

SENDER_MAP = load_sender_mapping()

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

def get_label_for_sender(fr, subj):
    # Try mapping by sender key
    name, domain = parse_email_address(fr)
    email_key = f"{name} <{domain}>" if name else domain
    if email_key in SENDER_MAP:
        return SENDER_MAP[email_key]
    # Fallback: create a generic Sweep label based on domain or name
    if name:
        safe = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip()[:30] or 'Unknown'
        return f"Sweep/{safe}"
    elif domain:
        safe = domain.replace('.', '-')
        return f"Sweep/{safe}"
    else:
        return "Sweep/Unread"

import re
def get_label_for_sender(fr, subj):
    name, domain = parse_email_address(fr)
    email_key = f"{name} <{domain}>" if name else domain
    if email_key in SENDER_MAP:
        return SENDER_MAP[email_key]
    # Fallback: use domain-derived label
    if domain:
        safe = re.sub(r'[^a-zA-Z0-9-]', '-', domain)
        safe = re.sub(r'-+', '-', safe).strip('-')
        return f"Sweep/{safe}" if safe else "Sweep/Unknown"
    elif name:
        safe = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
        safe = re.sub(r'\s+', '-', safe).strip('-')
        return f"Sweep/{safe}" if safe else "Sweep/Unknown"
    else:
        return "Sweep/Unknown"

def fetch(url):
    cmd = ['curl', '-s', '-f', '-H', f'Authorization: Bearer {API_KEY}', url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def get_label_id(label_name):
    # Check cache
    try:
        with open(LABEL_CACHE_FILE) as f:
            cache = json.load(f)
    except Exception:
        cache = {}
    if label_name in cache:
        return cache[label_name]
    # Fetch existing labels from Gmail
    labels_url = "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels"
    resp = fetch(labels_url)
    if resp:
        try:
            labels = json.loads(resp).get('labels', [])
            for lbl in labels:
                if lbl.get('name') == label_name:
                    cache[label_name] = lbl['id']
                    with open(LABEL_CACHE_FILE, 'w') as f:
                        json.dump(cache, f, indent=2)
                    return lbl['id']
        except Exception:
            pass
    # Create label
    create_url = "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels"
    payload = {"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    cmd = ['curl', '-s', '-f', '-X', 'POST', '-H', 'Content-Type: application/json', '-H', f'Authorization: Bearer {API_KEY}', '-d', json.dumps(payload), create_url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            lbl = json.loads(result.stdout)
            label_id = lbl.get('id')
            if label_id:
                cache[label_name] = label_id
                with open(LABEL_CACHE_FILE, 'w') as f:
                    json.dump(cache, f, indent=2)
                return label_id
        except Exception:
            pass
    return None

def apply_label(msg_id, label_id):
    url = f"https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/{msg_id}/modify"
    payload = {"addLabelIds": [label_id], "removeLabelIds": ["UNREAD"]}
    cmd = ['curl', '-s', '-f', '-X', 'POST', '-H', 'Content-Type: application/json', '-H', f'Authorization: Bearer {API_KEY}', '-d', json.dumps(payload), url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

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
        label_name = get_label_for_sender(from_hdr, subj_hdr)
        counts[label_name] = counts.get(label_name, 0) + 1
        label_id = get_label_id(label_name)
        if label_id:
            if apply_label(msg_id, label_id):
                log(f"Labeled {msg_id} as {label_name}")
            else:
                log(f"Failed to label {msg_id}")
        else:
            log(f"No label ID for {label_name}")
    total = sum(counts.values())
    for k, v in counts.items():
        log(f"{k}: {v}")
    summary = f"📧 Email batch: {total} unread"
    for k, v in counts.items():
        summary += f"\n  - {k}: {v}"
    print(summary)
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
