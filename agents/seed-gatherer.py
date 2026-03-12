#!/usr/bin/env python3
import os, sys, json, subprocess, time, uuid, datetime, timezone
from typing import List, Dict

# Config
MATON_API_KEY = os.getenv('MATON_API_KEY')
if not MATON_API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
BASE_URL = "https://gateway.maton.ai/google-mail/gmail/v1/users/me"
SEEDS_FILE = '/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl'
RSS_FEEDS = [
    'https://rss.arxiv.org/rss/cs.AI',
    'https://rss.arxiv.org/rss/cs.CL',
    'https://rss.arxiv.org/rss/cs.LG',
    'https://rss.arxiv.org/rss/cs.SE',
    'https://techcrunch.com/feed/',
    'https://www.theverge.com/rss/index.xml',
]
MAX_EMAILS = 50  # per run

def log(msg):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}")

def fetch_url(url):
    cmd = ['curl', '-s', '-f', url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    return res.stdout

def fetch_unread_emails(limit=50):
    ids = []
    page_token = None
    while len(ids) < limit:
        url = f"{BASE_URL}/messages?q=is:unread&maxResults=50"
        if page_token:
            url += f"&pageToken={page_token}"
        resp = fetch_url(url)
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
            log(f"JSON error (emails): {e}")
            break
    return ids

def fetch_email(msg_id):
    url = f"{BASE_URL}/messages/{msg_id}?format=full"
    resp = fetch_url(url)
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

def extract_seed_from_email(msg):
    from_hdr = get_header(msg, 'From')
    subj_hdr = get_header(msg, 'Subject')
    snippet = msg.get('snippet', '')[:200]
    ts = msg.get('internalDate', '')
    seed = {
        "id": str(uuid.uuid4()),
        "title": subj_hdr or "(No subject)",
        "snippet": snippet,
        "source": f"email:{from_hdr}",
        "tags": ["email"],
        "ts": datetime.datetime.utcfromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S') if ts else datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    }
    return seed

def fetch_rss(url):
    xml = fetch_url(url)
    if not xml:
        return []
    # Very simple parsing
    seeds = []
    try:
        import re
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        for item in items[:10]:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
            link_match = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL)
            desc_match = re.search(r'<description[^>]*>(.*?)</description>', item, re.DOTALL)
            if title_match and link_match:
                title = title_match.group(1).strip()
                link = link_match.group(1).strip()
                desc = desc_match.group(1).strip() if desc_match else ''
                seeds.append({
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "snippet": desc[:200],
                    "source": f"rss:{url}",
                    "tags": ["rss"],
                    "ts": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                })
    except Exception as e:
        log(f"RSS parse error for {url}: {e}")
    return seeds

def main():
    log("Seed gatherer starting")
    total_new = 0
    # 1. Gather unread emails
    ids = fetch_unread_emails(MAX_EMAILS)
    log(f"Fetched {len(ids)} unread emails")
    for msg_id in ids:
        msg = fetch_email(msg_id)
        if msg:
            seed = extract_seed_from_email(msg)
            with open(SEEDS_FILE, 'a') as f:
                f.write(json.dumps(seed) + '\n')
            total_new += 1
    # 2. Gather RSS feeds
    for url in RSS_FEEDS:
        rss_seeds = fetch_rss(url)
        for seed in rss_seeds:
            with open(SEEDS_FILE, 'a') as f:
                f.write(json.dumps(seed) + '\n')
            total_new += 1
    log(f"Added {total_new} seeds to {SEEDS_FILE}")

if __name__ == '__main__':
    main()
