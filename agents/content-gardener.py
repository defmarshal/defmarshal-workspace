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
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_content.jsonl')
CONTENT_DIR = Path('/home/ubuntu/.openclaw/workspace/content')
GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
OPENCLAWS = '/home/ubuntu/.npm-global/bin/openclaw'

CONTENT_DIR.mkdir(parents=True, exist_ok=True)

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
    graph['nodes'].append({"id": output_path, "type": "content", "title": title})
    # Add edge
    graph['edges'].append({"from": seed_id, "to": output_path, "type": "produced"})
    save_graph(graph)

def generate_text(prompt: str, system_msg: str = "You are a helpful assistant.") -> str:
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        log("OPENROUTER_API_KEY not set")
        return ''
    payload = {
        'model': 'stepfun/step-3.5-flash:free',
        'messages': [
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 1024,
        'temperature': 0.7
    }
    cmd = [
        'curl',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload),
        'https://openrouter.ai/api/v1/chat/completions'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            log(f"Curl error {result.returncode}: {result.stderr[:200]}")
            return ''
        data = json.loads(result.stdout)
        if 'error' in data:
            log(f"OpenRouter error: {data['error'].get('message', 'unknown')}")
            return ''
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        log(f"OpenRouter request failed: {e}")
        return ''

def generate_content(seed) -> str:
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    slug = seed['title'].lower().replace(' ', '-')[:80]
    filename = CONTENT_DIR / f"{today}-{slug}.md"
    prompt = f"""Write a friendly, insightful blog post titled "{seed['title']}".
Context:
{seed['snippet']}

Make it engaging, with a short intro, key points, and a conclusion. Use markdown. Keep under 500 words."""
    body = generate_text(prompt, system_msg="You are a tech blogger. Write engaging, human‑written style content with a kawaii touch when appropriate.")
    if not body:
        body = f"{seed['snippet']}\n\n*(Auto‑draft placeholder)*"
    content = f"""# {seed['title']}

**Source:** {seed['source']}

{body}
"""
    with open(filename, 'w') as f:
        f.write(content)
    return str(filename)

def main():
    seeds = load_seeds()
    processed = load_processed()
    unprocessed = [s for s in seeds if s['id'] not in processed]
    if not unprocessed:
        log("No new seeds for content gardening")
        return
    # Pick most recent seed
    unprocessed.sort(key=lambda s: s['ts'], reverse=True)
    seed = unprocessed[0]
    log(f"Growing content for seed: {seed['title']}")
    output_path = generate_content(seed)
    add_graph_edge(seed['id'], output_path, seed['title'])
    mark_processed(seed['id'])
    log(f"Content written to {output_path}")

if __name__ == '__main__':
    main()
