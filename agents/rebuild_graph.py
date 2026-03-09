#!/usr/bin/env python3
import os, sys, json, datetime, re
from pathlib import Path

GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_seeds.jsonl')
RESEARCH_DIR = Path('/home/ubuntu/.openclaw/workspace/research')
CONTENT_DIR = Path('/home/ubuntu/.openclaw/workspace/content')

def log(msg):
    print(msg)

def load_seeds():
    seeds = {}
    with open(SEEDS_FILE) as f:
        for line in f:
            s = json.loads(line)
            seeds[s['id']] = s
    return seeds

def load_processed():
    processed = set()
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            for line in f:
                p = json.loads(line)
                processed.add(p['id'])
    return processed

def find_output_files():
    outputs = []
    for d in [RESEARCH_DIR, CONTENT_DIR]:
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and f.name.startswith('2026-'):
                    # Try to extract seed ID from filename? Not stored. We'll just list outputs.
                    outputs.append(str(f))
    return outputs

def build_graph():
    seeds = load_seeds()
    processed = load_processed()
    outputs = find_output_files()
    graph = {"nodes": [], "edges": []}
    # Add seed nodes
    for seed_id, seed in seeds.items():
        graph['nodes'].append({
            "id": seed_id,
            "type": "seed",
            "title": seed.get('title')
        })
    # Add output nodes and edges: we don't know which seed produced which output reliably without explicit mapping.
    # We'll create edges only for processed seeds that have corresponding output by date heuristic.
    # For now, just add output nodes.
    for outp in outputs:
        graph['nodes'].append({
            "id": outp,
            "type": "output",
            "title": Path(outp).name
        })
    # Save
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, indent=2)
    log(f"Graph rebuilt: {len(graph['nodes'])} nodes ({len(seeds)} seeds, {len(outputs)} outputs)")

if __name__ == '__main__':
    build_graph()
