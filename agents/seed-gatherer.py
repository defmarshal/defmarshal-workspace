#!/usr/bin/env python3
"""Seed Gatherer - Collects seeds from RSS feeds and optionally email."""

import os
import json
import datetime
import feedparser
from pathlib import Path

# Configuration
WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
SEEDS_FILE = MEMORY_DIR / "seeds.jsonl"
LOG_FILE = MEMORY_DIR / "seed-gatherer.log"

# RSS feeds to monitor (arXiv categories + tech news)
RSS_FEEDS = [
    "http://export.arxiv.org/rss/cs.AI",
    "http://export.arxiv.org/rss/cs.CL",
    "http://export.arxiv.org/rss/cs.LG",
    "http://export.arxiv.org/rss/cs.SE",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]

def log(msg):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[{timestamp}] {msg}", flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def fetch_rss_feed(url):
    """Fetch and parse an RSS feed."""
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        log(f"ERROR: Failed to fetch {url}: {e}")
        return []

def collect_seeds():
    """Collect seeds from all RSS feeds."""
    all_seeds = []
    
    for url in RSS_FEEDS:
        log(f"Fetching RSS feed: {url}")
        entries = fetch_rss_feed(url)
        for entry in entries:
            # Create a seed item
            seed = {
                "id": entry.get('id', entry.get('link', '')),
                "title": entry.get('title', ''),
                "summary": entry.get('summary', '')[:200],
                "link": entry.get('link', ''),
                "published": entry.get('published', ''),
                "source": url,
            }
            all_seeds.append(seed)
    
    return all_seeds

def append_seeds_to_file(seeds):
    """Append new seeds to the seeds file."""
    if not seeds:
        return 0
    
    # Keep track of existing seeds to avoid duplicates
    existing_ids = set()
    if SEEDS_FILE.exists():
        try:
            with open(SEEDS_FILE) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            if isinstance(data, dict) and 'id' in data:
                                existing_ids.add(data['id'])
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            log(f"WARNING: Could not read existing seeds: {e}")
    
    # Filter out duplicates and append new ones
    new_count = 0
    with open(SEEDS_FILE, 'a') as f:
        for seed in seeds:
            seed_id = seed['id']
            if seed_id not in existing_ids:
                f.write(json.dumps(seed) + '\n')
                existing_ids.add(seed_id)
                new_count += 1
    
    return new_count

def main():
    log("Seed gatherer started")
    
    # Ensure memory directory exists
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Collect seeds from RSS feeds
    seeds = collect_seeds()
    log(f"Collected {len(seeds)} potential seeds from RSS feeds")
    
    if not seeds:
        log("No seeds collected, exiting")
        return
    
    # Append to file
    new_count = append_seeds_to_file(seeds)
    log(f"Added {new_count} new seeds to {SEEDS_FILE}")
    
    # Count total seeds
    total = 0
    if SEEDS_FILE.exists():
        with open(SEEDS_FILE) as f:
            total = sum(1 for line in f if line.strip())
    
    log(f"Total seeds in database: {total}")
    log("Seed gatherer finished")

if __name__ == "__main__":
    main()
