#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess
from datetime import UTC
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
    print(f"[{datetime.datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}")

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
        f.write(json.dumps({"id": seed_id, "processed_at": datetime.datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}) + '\n')

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

def sanitize_identifier(name: str) -> str:
    """Make a valid Python identifier: remove colons, punctuation, spaces."""
    name = name.replace(':', '').replace(',', '').replace('.', '').replace(' ', '_').replace('-', '_')
    name = ''.join(c if c.isalnum() or c == '_' else '' for c in name)
    if not name:
        return 'concept'
    if name[0].isdigit():
        name = '_' + name
    return name.lower()

def create_fallback_script(seed):
    """Generate a meaningful script when the agent fails, based on seed title and snippet."""
    title = seed['title']
    snippet = seed.get('snippet', '')[:500]
    
    # Extract key terms for context
    key_terms = []
    for word in title.replace(',', '').replace('.', '').split():
        if len(word) > 3 and word.lower() not in ['this', 'that', 'with', 'from', 'what', 'when', 'were', 'have', 'been', 'were', 'they', 'their']:
            key_terms.append(word)
    
    top_terms = key_terms[:3] if key_terms else ['concept']
    
    # Prepare sanitized identifiers and literals
    term0 = top_terms[0]
    term1 = top_terms[1] if len(top_terms) > 1 else 'data'
    class_name = sanitize_identifier(term0.title()) + "Concept"
    func_demonstrate = "demonstrate_" + sanitize_identifier(term0)
    func_analyze = "analyze_" + sanitize_identifier(term1)
    
    script = f'''#!/usr/bin/env python3
"""
Auto-generated script (fallback) for: {title}
This demonstrates the core concept from: {snippet[:100]}...
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict

SCRIPT_TITLE = {title!r}
TERM_0 = {term0!r}
TERM_1 = {term1!r}

@dataclass
class {class_name}:
    """Representation of: {term0}"""
    value: float
    description: str
    
def {func_demonstrate}(iterations: int = 5):
    """Core demonstration of {term0} concept."""
    print(f"Demonstrating: {{SCRIPT_TITLE}}")
    print("=" * 50)
    
    concepts = []
    for i in range(min(iterations, 5)):
        concept = {class_name}(
            value=random.uniform(0.1, 1.0),
            description=f"{{TERM_0}} instance {{i+1}}"
        )
        concepts.append(concept)
        print(f"{{i+1}}. {{concept.description}} -> value: {{concept.value:.3f}}")
        time.sleep(0.2)
    
    # Analysis
    avg_value = sum(c.value for c in concepts) / len(concepts)
    print(f"\\nAverage {{TERM_0}} strength: {{avg_value:.3f}}")
    
    return concepts

def {func_analyze}(data: List) -> Dict:
    """Analyze {{TERM_1}} patterns."""
    if not data:
        return {{"error": "No data"}}
    
    values = [d.value if hasattr(d, 'value') else float(d) for d in data]
    return {{
        "count": len(values),
        "mean": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
        "range": max(values) - min(values)
    }}

def main():
    print(f"Script: {{SCRIPT_TITLE}}")
    print(f"Key concepts: {', '.join(top_terms)}")
    print("-" * 40)
    
    # Run demonstration
    data = {func_demonstrate}()
    
    # Analysis
    analysis = {func_analyze}(data)
    print(f"\\nAnalysis: {{analysis}}")
    
    print("\\n" + "=" * 50)
    print("This fallback script demonstrates the core idea")
    print("using structured data and analysis functions.")
    print("For a more sophisticated implementation,")
    print("ensure OpenRouter connectivity is available.")

if __name__ == "__main__":
    main()
'''
    
    return script

def generate_app(seed):
    prompt = f"""Write a small, practical Python script based on this idea:

Title: {seed['title']}
Context: {seed['snippet']}

The script should be self-contained, include a shebang, and demonstrate the concept. Keep it under 100 lines. Output only the code, no explanations."""
    code = generate_code_via_agent(prompt)
    
    # Enhanced fallback: create a meaningful script based on seed content
    if not code or len(code) < 20:
        log(f"Agent returned insufficient code (length {len(code) if code else 0}), using enhanced fallback")
        code = create_fallback_script(seed)
    
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
