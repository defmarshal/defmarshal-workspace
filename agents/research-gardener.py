#!/usr/bin/env python3
import os, sys, json, uuid, datetime, subprocess, urllib.request, urllib.error, ssl
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

def tavily_search(query: str, api_key: str, max_results: int = 10) -> str:
    """Perform a web search via Tavily API and return a formatted string of results."""
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "search_depth": "basic",
        "topic": "general",
        "max_results": max_results,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        # Use default SSL context
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return f"_Search error: HTTP {resp.status}_"
            resp_data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "_Search error: Invalid Tavily API key_"
        elif e.code == 429:
            return "_Search error: Rate limit exceeded_"
        else:
            return f"_Search error: HTTP {e.code}_"
    except urllib.error.URLError as e:
        return f"_Search error: Connection failed ({e.reason})_"
    except Exception as e:
        return f"_Search error: {str(e)}_"

    # Format results
    parts = []
    if resp_data.get("answer"):
        parts.append("**AI Answer:**\n" + resp_data["answer"] + "\n")
    results = resp_data.get("results", [])
    if results:
        parts.append("**Top Results:**")
        for i, item in enumerate(results, 1):
            title = item.get('title', 'No title')
            url = item.get('url', '')
            content = item.get('content', '').strip()
            line = f"{i}. [{title}]({url})"
            if content:
                # Shorten snippet
                snippet = content[:300] + ("..." if len(content) > 300 else "")
                line += f"\n   {snippet}"
            parts.append(line)
    return "\n\n".join(parts) if parts else "_No results found_"

def generate_report(seed: Dict[str, Any]) -> str:
    query = seed['title']
    log(f"Searching for: {query}")
    # Attempt Tavily search if API key is available
    api_key = os.getenv('TAVILY_API_KEY')
    if api_key:
        search_results = tavily_search(query, api_key, max_results=10)
    else:
        log("TAVILY_API_KEY not set; skipping web search")
        search_results = '_Web search skipped (no API key configured)._'

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

{search_results}

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
