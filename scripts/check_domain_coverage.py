#!/usr/bin/env python3
"""
Domain Coverage Monitor — quick health check for research-gardener
Usage: python3 scripts/check_domain_coverage.py
"""

import os
import json
from collections import Counter
from datetime import datetime, timezone

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(WORKSPACE, 'research')
SEEDS_FILE = os.path.join(WORKSPACE, 'memory', 'seeds.jsonl')
PROCESSED_FILE = os.path.join(WORKSPACE, 'memory', 'processed_seeds.jsonl')

DOMAIN_KEYWORDS = {
    'anime': ['anime', 'manga', 'animation'],
    'banking': ['bank', 'finance', 'fintech', 'payment'],
    'tech': ['tech', 'hardware', 'chip', 'processor', 'cloud'],
    'ai': ['ai', 'ml', 'llm', 'agent', 'gpt'],
    'security': ['security', 'cyber', 'privacy', 'encrypt', 'vulnerab']
}

def get_today_reports():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    reports = []
    for f in os.listdir(RESEARCH_DIR):
        if f.startswith(today) and f.endswith('.md'):
            reports.append(f)
    return reports

def classify_title(title):
    title_l = title.lower()
    matches = []
    for dom, kws in DOMAIN_KEYWORDS.items():
        if any(kw in title_l for kw in kws):
            matches.append(dom)
    return matches if matches else ['unclassified']

def main():
    print(f"=== Domain Coverage Monitor ===")
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    reports = get_today_reports()
    print(f"Date: {today}")
    print(f"Reports found: {len(reports)}\n")

    if reports:
        domain_counts = Counter()
        for f in sorted(reports, key=lambda x: os.path.getmtime(os.path.join(RESEARCH_DIR, x)), reverse=True):
            # Remove date prefix and .md suffix to get slug, but better to derive from filename's slug part
            slug = f[len(today)+1:-3]  # after "YYYY-MM-DD-"
            domains = classify_title(slug)
            for d in domains:
                domain_counts[d] += 1
            print(f"- {f} -> {', '.join(domains)}")
        print(f"\nDomain coverage: {dict(domain_counts)}")
        all_domains = set(DOMAIN_KEYWORDS.keys())
        covered = set(d for d in all_domains if domain_counts.get(d,0) > 0)
        missing = all_domains - covered
        if missing:
            print(f"⚠️  Missing domains: {', '.join(sorted(missing))}")
        else:
            print("✅ All domains covered!")
    else:
        print("No reports for today yet.")

    # Seed health
    print("\n=== Seed Pool Status ===")
    processed = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE) as f:
            for line in f:
                if line.strip():
                    processed.add(json.loads(line)['id'])
    unprocessed = []
    if os.path.exists(SEEDS_FILE):
        with open(SEEDS_FILE) as f:
            for line in f:
                if not line.strip(): continue
                s = json.loads(line)
                if s['id'] not in processed:
                    unprocessed.append(s)
    total_unprocessed = len(unprocessed)
    print(f"Total unprocessed seeds: {total_unprocessed}")
    # Count by domain
    domain_seed_counts = Counter()
    for s in unprocessed:
        title = s.get('title','').lower()
        for dom, kws in DOMAIN_KEYWORDS.items():
            if any(kw in title for kw in kws):
                domain_seed_counts[dom] += 1
                break
    for dom in sorted(DOMAIN_KEYWORDS.keys()):
        count = domain_seed_counts.get(dom,0)
        marker = "❗ EXHAUSTED" if count == 0 else ""
        print(f"  {dom}: {count} {marker}")

if __name__ == '__main__':
    main()
