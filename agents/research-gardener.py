#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess
from pathlib import Path
from typing import Dict, Any

# Paths
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_seeds.jsonl')
RESEARCH_DIR = Path('/home/ubuntu/.openclaw/workspace/research')
GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
OPENCLAWS = '/home/ubuntu/.npm-global/bin/openclaw'

RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    print(f"[{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}")

def load_seeds():
    seeds = []
    with open(SEEDS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds

def load_processed():
    processed = set()
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    processed.add(json.loads(line)['id'])
    return processed

def mark_processed(seed_id: str):
    with open(PROCESSED_FILE, 'a') as f:
        f.write(json.dumps({"id": seed_id, "processed_at": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) + '\n')

def load_graph():
    if GRAPH_FILE.exists():
        with open(GRAPH_FILE) as f:
            return json.load(f)
    return {"nodes": [], "edges": []}

def save_graph(graph):
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, indent=2)

def add_graph_edge(seed_id: str, output_path: str, title: str):
    graph = load_graph()
    # Add seed node if missing
    if not any(n.get('id') == seed_id for n in graph['nodes']):
        graph['nodes'].append({"id": seed_id, "type": "seed", "title": title})
    # Add output node
    graph['nodes'].append({"id": output_path, "type": "output", "title": title})
    # Add edge
    graph['edges'].append({"from": seed_id, "to": output_path, "type": "produced"})
    save_graph(graph)

def call_tavily(query: str) -> str:
    # Use openclaw web search via Tavily skill (if available)
    # In practice, we can shell out to `openclaw web search "<query>"` and parse results.
    # For simplicity, use curl to Tavily if API key set, else fallback to generic.
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
    if TAVILY_API_KEY:
        import requests
        resp = requests.post('https://api.tavily.com/search', json={
            'api_key': TAVILY_API_KEY,
            'query': query,
            'max_results': 10,
            'include_raw_content': False
        }, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            # Concatenate results
            snippets = []
            for r in data.get('results', [])[:5]:
                snippets.append(f"- {r.get('title')}: {r.get('snippet')}")
            return '\n'.join(snippets) if snippets else 'No results'
        else:
            log(f"Tavily error {resp.status_code}")
            return ''
    else:
        # Fallback: use openclaw web search via exec
        try:
            result = subprocess.run([OPENCLAWS, 'web', 'search', query], capture_output=True, text=True, timeout=30)
            return result.stdout.strip() or result.stderr.strip() or 'Search completed.'
        except Exception as e:
            log(f"OpenClaw web search failed: {e}")
            return ''

def generate_report(seed: Dict[str, Any]) -> str:
    # Perform a quick literature review
    query = seed['title']
    log(f"Searching for: {query}")
    search_results = call_tavily(query)
    # Build markdown report
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    slug = seed['title'].lower().replace(' ', '-')[:50]
    filename = RESEARCH_DIR / f"{today}-{slug}.md"
    content = f"""# {seed['title']}

**Seed ID:** {seed['id']}  
**Source:** {seed['source']}  
**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

{seed['snippet']}

## Findings

{search_results if search_results else '_No additional findings._'}

## References

- Seed:: {seed['id']}
"""
    with open(filename, 'w') as f:
        f.write(content)
    return str(filename)

def main():
    seeds = load_seeds()
    processed = load_processed()
    unprocessed = [s for s in seeds if s['id'] not in processed]
    if not unprocessed:
        log("No new seeds to research")
        return
    # Pick the most recent seed (highest timestamp)
    unprocessed.sort(key=lambda s: s['ts'], reverse=True)
    seed = unprocessed[0]
    log(f"Researching seed: {seed['title']}")
    output_path = generate_report(seed)
    add_graph_edge(seed['id'], output_path, seed['title'])
    mark_processed(seed['id'])
    log(f"Report written to {output_path}")

if __name__ == '__main__':
    main()
