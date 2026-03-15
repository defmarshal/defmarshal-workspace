#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess, signal
from pathlib import Path

# Paths
SEEDS_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/seeds.jsonl')
PROCESSED_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/processed_seeds.jsonl')
CONTENT_DIR = Path('/home/ubuntu/.openclaw/workspace/content')
GRAPH_FILE = Path('/home/ubuntu/.openclaw/workspace/memory/graph.json')
OPENCLAWS = '/home/ubuntu/.npm-global/bin/openclaw'

CONTENT_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}", flush=True)

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
    graph['nodes'].append({"id": output_path, "type": "content", "title": title})
    # Add edge
    graph['edges'].append({"from": seed_id, "to": output_path, "type": "produced"})
    save_graph(graph)

def generate_content(seed) -> str:
    # Use openclaw content generation via a simple agent turn
    # Use Popen with process group to ensure we can kill hung subprocesses
    today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    slug = seed['title'].lower().replace(' ', '-')[:80]
    filename = CONTENT_DIR / f"{today}-{slug}.md"
    # Call an LLM to write a blog post — use a no-nonsense agent turn
    prompt = f"""Write a blog post titled "{seed['title']}".

Context from source:
{seed['snippet']}

Requirements:
- Friendly yet insightful tone
- Engaging intro paragraph
- 3-5 key points as subheadings or bullets
- Short conclusion
- Use markdown formatting

IMPORTANT: Output ONLY the raw markdown content. No extra commentary, no "Here's your blog post", no confirmations. Just the markdown."""
    try:
        # Start subprocess in its own process group so we can kill the whole group
        proc = subprocess.Popen([OPENCLAWS, 'agent', '--local', '--agent', 'main', '--message', prompt],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                preexec_fn=os.setsid)
        try:
            stdout, stderr = proc.communicate(timeout=60)
            content = stdout.strip()
            if not content:
                # Fallback: simple draft
                content = f"""# {seed['title']}

**Source:** {seed['source']}

{seed['snippet']}

*This article will be fleshed out by the content-gardener.*"""
        except subprocess.TimeoutExpired:
            # Kill the entire process group
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                pass
            # Wait a bit and force kill if still alive
            try:
                proc.wait(timeout=5)
            except Exception:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    pass
            log(f"Agent generation timed out after 60 seconds for seed: {seed['title']}")
            content = f"""# {seed['title']}

{seed['snippet']}

*(Auto-draft placeholder due to timeout)*"""
    except Exception as e:
        log(f"Agent generation failed: {e}")
        content = f"""# {seed['title']}

{seed['snippet']}

*(Auto-draft placeholder due to error)*"""
    # Write content to file
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
