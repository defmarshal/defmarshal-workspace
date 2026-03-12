#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess
from pathlib import Path
from collections import Counter

# Paths
GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PLANNER_OUT = Path('/home/ubuntu/.openclaw/workspace/memory/planner_suggestions.jsonl')

def log(msg):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}")

def load_graph():
    if GRAPH_FILE.exists():
        with open(GRAPH_FILE) as f:
            return json.load(f)
    return {"nodes": [], "edges": []}

def load_seeds():
    seeds = []
    with open(SEEDS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds

def analyze_interest_profile(seeds):
    # Aggregate tags from seeds
    tag_counts = Counter()
    for seed in seeds:
        for tag in seed.get('tags', []):
            tag_counts[tag] += 1
    return tag_counts

def suggest_new_seeds(tag_counts):
    # Define target areas we want to cover (based on interests)
    target_categories = {
        'ai': ['ai', 'machine learning', 'llm', 'agent', 'gpt', 'transformer'],
        'space': ['space', 'rocket', 'satellite', 'iss', 'starlink', 'spacex', 'nasa'],
        'quantum': ['quantum', 'qubit', 'quantum computing', 'quantum algorithm'],
        'web': ['web', 'frontend', 'backend', 'javascript', 'react', 'vue', 'node'],
        'infra': ['devops', 'kubernetes', 'docker', 'aws', 'cloud', 'serverless', 'ci/cd'],
        'tech': ['tech', 'startup', 'silicon valley', 'funding', 'product'],
    }
    # Find under-represented categories
    suggestions = []
    for cat, keywords in target_categories.items():
        cat_count = sum(tag_counts.get(k, 0) for k in keywords)
        if cat_count < 3:  # arbitrary threshold; suggest more
            # Generate a sample query to seed
            if cat == 'ai':
                query = "latest transformer architectures 2025"
            elif cat == 'space':
                query = "starlink v2 launch schedule"
            elif cat == 'quantum':
                query = "quantum error correction breakthroughs"
            elif cat == 'web':
                query = "react server components vs traditional rendering"
            elif cat == 'infra':
                query = "kubernetes autoscaling best practices 2025"
            elif cat == 'tech':
                query = "AI startup funding trends Q1 2025"
            else:
                query = f"latest developments in {cat}"
            suggestions.append({
                "id": str(uuid.uuid4()),
                "title": f"Planner suggestion: {query}",
                "snippet": f"Under‑represented category '{cat}'. Query: {query}",
                "source": "planner",
                "tags": ["planner", cat],
                "ts": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            })
    return suggestions

def main():
    log("Planner starting")
    seeds = load_seeds()
    tag_counts = analyze_interest_profile(seeds)
    log(f"Current tag profile: {dict(tag_counts.most_common(10))}")
    new_seeds = suggest_new_seeds(tag_counts)
    log(f"Generated {len(new_seeds)} planner suggestions")
    # Append suggestions to seeds file (they become real seeds for gatherer to consider)
    with open(SEEDS_FILE, 'a') as f:
        for s in new_seeds:
            f.write(json.dumps(s) + '\n')
    # Also record suggestions separately for audit
    with open(PLANNER_OUT, 'a') as f:
        for s in new_seeds:
            f.write(json.dumps(s) + '\n')
    log("Planner complete")

if __name__ == '__main__':
    main()
