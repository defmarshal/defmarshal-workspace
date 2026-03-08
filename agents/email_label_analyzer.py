#!/usr/bin/env python3
import os, sys, json, subprocess, time, re
from collections import defaultdict
from typing import Dict, List, Tuple

# Config
MATON_API_KEY = os.getenv('MATON_API_KEY')
if not MATON_API_KEY:
    print("MATON_API_KEY not set")
    sys.exit(1)
BASE_URL = "https://gateway.maton.ai/google-mail/gmail/v1/users/me"
STATE_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_analyzer.state'
OUTPUT_FILE = '/home/ubuntu/.openclaw/workspace/memory/label_mapping.json'
LOG_FILE = '/home/ubuntu/.openclaw/workspace/memory/email_analyzer.log'

MAX_UNREAD = int(os.getenv('MAX_UNREAD', '1000'))  # limit for analysis

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

def parse_email_address(addr: str) -> Tuple[str, str]:
    # Very simple: "Name <email@domain.com>" or "email@domain.com"
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

def categorize_sender(name: str, domain: str, subject: str) -> str:
    # Normalize
    name_l = name.lower()
    domain_l = domain.lower()
    subject_l = subject.lower()
    # Keywords
    BANKING_SENDERS = ['bca', 'bank', 'mandiri', 'bni', 'bri', 'seacon', 'cimb', 'danamon', 'permata', 'ocbc', 'uob', 'hsbc', 'citibank', 'standard chartered', 'maybank', 'btn', 'btpn', 'sinarmas', 'mega', 'bukopin', 'panin', 'noci', 'dbs', 'sumitomo', 'mizuho', 'mufg', 'credit card', 'visa', 'mastercard']
    BANKING_DOMAINS = ['bca.co.id', 'bankmandiri.co.id', 'bni.co.id', 'bri.co.id', 'bankbca.com', 'cimb.com', 'danamon.co.id', 'permata.com', 'ocbc.co.id', 'uob.co.id', 'hsbc.co.id', 'citibank.com', 'maybank.co.id', 'btn.co.id']
    ALERT_SENDERS = ['alert', 'error', 'monitoring', 'system', 'security', 'aws', 'gcp', 'google cloud', 'azure', 'datadog', 'new relic', 'pagerduty', 'opsgenie', 'grafana', 'prometheus', 'sentry', 'logrocket', 'rollbar', 'bugsnag', 'uptime', 'status', 'incident', 'outage']
    ALERT_DOMAINS = ['aws.amazon.com', 'console.aws.amazon.com', 'cloud.google.com', 'azure.microsoft.com', 'datadoghq.com', 'newrelic.com', 'pagerduty.com', 'opsgenie.com', 'grafana.com', 'sentry.io']
    WORK_DOMAINS = ['company.com', 'company.org', 'work.com', 'corp.', 'internal', 'office.', 'enterprise.', 'business.']
    NEWSLETTER_SUBJECT = ['newsletter', 'digest', 'promo', 'marketing', 'subscribe', 'daily', 'weekly', 'deals', 'offers']
    HR_SUBJECT = ['hr', 'payroll', 'leave', 'timesheet', 'benefits', 'talent', 'recruitment', 'onboarding', 'offboarding']
    WORK_SUBJECT = ['meeting', 'sprint', 'planning', 'standup', 'review', 'retro', 'scrum', 'jira', 'confluence', 'slack', 'teams', 'zoom', 'sync', '1:1', 'one-on-one', 'team', 'project', 'deadline', 'deliverable', 'milestone', 'quarterly', 'weekly', 'monthly']
    # Decision order
    if any(x in domain_l for x in BANKING_DOMAINS) or any(x in name_l for x in BANKING_SENDERS):
        return 'banking'
    if any(x in domain_l for x in ALERT_DOMAINS) or any(x in name_l for x in ALERT_SENDERS) or any(x in subject_l for x in ['alert', 'error', 'warning', 'critical', 'incident', 'outage', 'downtime', 'failure', 'exception', 'timeout', 'threshold', 'breach']):
        return 'alerts'
    if any(x in domain_l for x in WORK_DOMAINS) or any(x in subject_l for x in WORK_SUBJECT) or any(x in name_l for x in ['meeting', 'sprint', 'planning', 'standup', 'review', 'retro', 'scrum', 'jira', 'confluence', 'slack', 'teams', 'zoom']):
        return 'work'
    if any(x in subject_l for x in NEWSLETTER_SUBJECT):
        return 'newsletters'
    if any(x in subject_l for x in HR_SUBJECT) or any(x in name_l for x in ['hr', 'payroll', 'leave', 'timesheet', 'benefits', 'talent']):
        return 'hr'
    return 'personal'

def analyze_emails():
    processed = load_processed()
    ids = fetch_unread_ids(MAX_UNREAD)
    # Filter already processed
    new_ids = [i for i in ids if i not in processed]
    log(f"Total unread: {len(ids)}; new to analyze: {len(new_ids)}")
    if not new_ids:
        log("Nothing new to analyze")
        return {}
    # Simple: map sender key -> category
    sender_to_cat: Dict[str, str] = {}
    for i, msg_id in enumerate(new_ids, 1):
        msg = fetch_message(msg_id)
        if not msg:
            continue
        from_hdr = get_header(msg, 'From')
        subject_hdr = get_header(msg, 'Subject')
        name, domain = parse_email_address(from_hdr)
        cat = categorize_sender(name, domain, subject_hdr)
        # Unique key: use email address only (domain or full email)
        email = f"{name} <{domain}>" if name else domain
        if email not in sender_to_cat:
            sender_to_cat[email] = cat
        processed.add(msg_id)
        if i % 10 == 0:
            log(f"Processed {i}/{len(new_ids)}")
            time.sleep(0.2)  # gentle
    # Build label mapping
    categories = {
        'banking': 'Sweep/banking',
        'alerts': 'Sweep/alerts',
        'work': 'Sweep/work',
        'newsletters': 'Sweep/newsletters',
        'hr': 'Sweep/hr',
        'personal': 'Sweep/personal'
    }
    label_mapping = {
        'categories': categories,
        'senders': sender_to_cat
    }
    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(label_mapping, f, indent=2)
    save_processed(processed)
    log(f"Analysis complete: {len(processed)} total processed, mapping saved to {OUTPUT_FILE}")
    # Print summary
    print("\n=== Label Analysis Summary ===")
    summary = defaultdict(int)
    for cat in sender_to_cat.values():
        summary[cat] += 1
    for cat in categories.keys():
        print(f"{cat}: {summary.get(cat, 0)} distinct senders")
    return label_mapping

if __name__ == '__main__':
    analyze_emails()
