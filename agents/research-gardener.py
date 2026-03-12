#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess, timezone
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
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}")

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
        f.write(json.dumps({"id": seed_id, "processed_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}) + '\n')

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

def generate_report(seed: Dict[str, Any]) -> str:
    # Perform a quick literature review using openclaw web search (Tavily)
    query = seed['title']
    log(f"Searching for: {query}")
    # Use openclaw web search via subprocess (leveraging Tavily skill if configured)
    try:
        search_cmd = [OPENCLAWS, 'web', 'search', query, '--count', '10']
        result = subprocess.run(search_cmd, capture_output=True, text=True, timeout=30)
        search_results = result.stdout.strip() or result.stderr.strip() or ''
    except Exception as e:
        log(f"Web search failed: {e}")
        search_results = ''

    # Build a draft report
    today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    slug = seed['title'].lower().replace(' ', '-')[:50]
    filename = RESEARCH_DIR / f"{today}-{slug}.md"
    draft = f"""# {seed['title']}

**Seed ID:** {seed['id']}  
**Source:** {seed['source']}  
**Generated:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

{seed['snippet']}

## Preliminary Findings

{search_results if search_results else '_No search results available yet._'}

## Next Steps

- Expand on key points
- Add references and citations
- Cross-check with additional sources
"""
    # Now use openclaw agent to enhance the report (add structure, insights, references)
    prompt = f"""You are a research analyst. Improve this draft report by:
- Filling in gaps with background knowledge
- Adding clear section headings and bullet points
- Including inline citations where possible (e.g., [来源], [1])
- Keeping tone客观 and informative

Return the full markdown with improvements. Do not include meta-commentary.

DRAFT:

{draft}
"""
    try:
        enhance_cmd = [OPENCLAWS, 'agent', 'ask', '--prompt', prompt]
        result = subprocess.run(enhance_cmd, capture_output=True, text=True, timeout=120)
        enhanced = result.stdout.strip()
        if enhanced and len(enhanced) > len(draft):
            content = enhanced
        else:
            content = draft
    except Exception as e:
        log(f"Agent enhancement failed: {e}")
        content = draft

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
