#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess
from pathlib import Path

# Load workspace .env if present
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ.setdefault(k, v)

# Paths
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_seeds.jsonl')
APPS_DIR = Path('/home/ubuntu/.openclaw/workspace/apps')
GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
OPENCLAWS = '/home/ubuntu/.npm-global/bin/openclaw'

APPS_DIR.mkdir(parents=True, exist_ok=True)

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
    graph['nodes'].append({"id": output_path, "type": "app", "title": title})
    # Add edge
    graph['edges'].append({"from": seed_id, "to": output_path, "type": "produced"})
    save_graph(graph)

def generate_code_via_agent(prompt: str, system_msg: str = "You are a coding assistant. Respond with only the Python code. No explanations or markdown fencing.") -> str:
    try:
        full_prompt = f"{system_msg}\n\n{prompt}"
        result = subprocess.run([OPENCLAWS, 'agent', 'ask', '--prompt', full_prompt], capture_output=True, text=True, timeout=60)
        output = result.stdout.strip()
        return output
    except Exception as e:
        log(f"OpenClaw agent call failed: {e}")
        return ''

def generate_app(seed):
    prompt = f"""Write a small, practical Python script based on this idea:

Title: {seed['title']}
Context: {seed['snippet']}

The script should be self-contained, include a shebang, and demonstrate the concept. Keep it under 100 lines. Output only the code, no explanations."""
    code = generate_code_via_agent(prompt)
    if not code or len(code) < 20:
        code = f"""#!/usr/bin/env python3
# Auto-generated script
# Seed: {seed['title']}
print("Hello from {seed['title']}!")"""
    # Determine filename
    safe_title = seed['title'].lower().replace(' ', '-')[:50]
    safe_title = ''.join(c if c.isalnum() or c in '-_' else '_' for c in safe_title)
    filename = APPS_DIR / f"{safe_title}.py"
    # Ensure unique
    counter = 1
    orig = filename
    while filename.exists():
        filename = APPS_DIR / f"{orig.stem}-{counter}{orig.suffix}"
        counter += 1
    with open(filename, 'w') as f:
        f.write(code)
    return str(filename)

def main():
    seeds = load_seeds()
    processed = load_processed()
    unprocessed = [s for s in seeds if s['id'] not in processed]
    if not unprocessed:
        log("No new seeds for code gardening")
        return
    # Pick most recent seed
    unprocessed.sort(key=lambda s: s['ts'], reverse=True)
    seed = unprocessed[0]
    log(f"Generating app for seed: {seed['title']}")
    output_path = generate_app(seed)
    add_graph_edge(seed['id'], output_path, seed['title'])
    mark_processed(seed['id'])
    log(f"App written to {output_path}")

if __name__ == '__main__':
    main()
