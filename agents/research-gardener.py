#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess
from pathlib import Path
from typing import Dict, Any

# Load workspace .env if present
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ.setdefault(k, v)

# Paths
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_research.jsonl')
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

def generate_text(prompt: str, system_msg: str = "You are a helpful research assistant. Output concise, factual markdown.") -> str:
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        log("OPENROUTER_API_KEY not set; skipping generation")
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

def call_tavily(query: str) -> str:
    # For initial research step, we'll do a quick web search via openrouter itself
    # Use a simpler prompt to get recent info; we can still use Tavily if key exists
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
            snippets = []
            for r in data.get('results', [])[:5]:
                snippets.append(f"- {r.get('title')}: {r.get('snippet')}")
            return '\n'.join(snippets) if snippets else 'No results'
        else:
            log(f"Tavily error {resp.status_code}")
            return ''
    else:
        # Fallback: simple web summary via OpenRouter
        prompt = f"Provide a brief summary of recent developments regarding: {query}"
        return generate_text(prompt, system_msg="You are a research analyst. Provide a concise summary with key points.")

def generate_report(seed: Dict[str, Any]) -> str:
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    slug = seed['title'].lower().replace(' ', '-')[:50]
    filename = RESEARCH_DIR / f"{today}-{slug}.md"
    # Try to expand findings via LLM or search
    summary = seed['snippet']
    findings = '_No additional findings available._'
    # If Tavily key exists, try search
    search_results = call_tavily(seed['title'])
    if search_results:
        findings = search_results
    else:
        # Try generating a short analysis
        analysis = generate_text(f"Write a 3-bullet analysis of: {seed['title']}. Context: {seed['snippet']}", system_msg="You are a research assistant. Provide concise insights.")
        if analysis:
            findings = analysis
    content = f"""# {seed['title']}

**Seed ID:** {seed['id']}  
**Source:** {seed['source']}  
**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

{summary}

## Findings

{findings}

## References

- Seed: {seed['id']}
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
