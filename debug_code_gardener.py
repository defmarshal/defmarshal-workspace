#!/usr/bin/env python3
import json

seeds = set()
processed = set()
graph_seeds = set()

with open('memory/seeds.jsonl') as f:
    seeds = {json.loads(l)['id'] for l in f if l.strip()}

with open('memory/processed_seeds.jsonl') as f:
    processed = {json.loads(l)['id'] for l in f if l.strip()}

g = json.load(open('memory/graph.json'))
graph_seeds = {n['id'] for n in g['nodes'] if n.get('type') == 'seed'}

print(f'Total seeds: {len(seeds)}')
print(f'Processed: {len(processed)}')
print(f'In graph: {len(graph_seeds)}')
print(f'Graph seeds all processed? {graph_seeds.issubset(processed)}')
print(f'Processed not in graph: {len(processed - graph_seeds)}')
print(f'Seeds not processed: {len(seeds - processed)}')
print(f'Graph seeds not in seeds? {len(graph_seeds - seeds)}')
