#!/usr/bin/env python3
"""Code Gardener - Generates apps from seed topics via OpenRouter API."""

import os
import sys
import json
import uuid
import datetime
import subprocess
from pathlib import Path

# Configuration
WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
APPS_DIR = WORKSPACE / "apps"
SEEDS_FILE = WORKSPACE / "memory" / "seeds.jsonl"
LOG_FILE = WORKSPACE / "memory" / "code-gardener.log"

def log(msg):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[{timestamp}] {msg}", flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def read_seeds():
    """Read seeds from jsonl file, returning a list of seed dicts."""
    if not SEEDS_FILE.exists():
        return []
    seeds = []
    with open(SEEDS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    seeds.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return seeds

def call_openrouter(seed_text, model="google/gemini-2.0-flash-exp"):
    """Call OpenRouter API to generate app from seed text."""
    import requests
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        log("ERROR: OPENROUTER_API_KEY environment variable not set")
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/openclaw/openclaw",
    }
    
    prompt = f"""Generate a Python script for the following seed/topic.

Title: Generate from seed: {seed_text[:100]}...

Create a self-contained Python script that:
1. Is useful and practical
2. Includes a shebang (#!/usr/bin/env python3)
3. Demonstrates the concept from the seed
4. Is under 100 lines
5. Outputs only the code, no explanations

Write only the Python code."""
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a code generation assistant. Generate practical Python scripts."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        # Extract code from markdown fencing if present
        lines = content.strip().split('\n')
        code_lines = []
        in_code = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                code_lines.append(line)
        return '\n'.join(code_lines).strip()
    except Exception as e:
        log(f"ERROR: OpenRouter request failed: {e}")
        return None

def write_app(source_code, seed_id, seed_text):
    """Write generated code to a file in the apps directory."""
    # Create a safe filename from the seed text
    safe_name = seed_text[:80].lower().replace(' ', '-').replace('_', '-')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-_')
    if not safe_name:
        safe_name = f"seed-{seed_id}"
    
    filename = f"{safe_name}.py"
    filepath = APPS_DIR / filename
    
    # If file exists, add a numeric suffix
    counter = 1
    original_filepath = filepath
    while filepath.exists():
        filepath = original_filepath.with_name(f"{original_filepath.stem}-{counter}.py")
        counter += 1
    
    with open(filepath, 'w') as f:
        f.write(source_code)
    
    log(f"App written to {filepath}")
    return filepath

def main():
    log("Code gardener started")
    
    # Ensure directories exist
    APPS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    seeds = read_seeds()
    if not seeds:
        log("No seeds found, exiting")
        return
    
    for seed in seeds:
        seed_id = seed.get('id', str(uuid.uuid4()))
        seed_text = seed.get('text', '')
        
        if not seed_text:
            continue
        
        log(f"Generating app for seed: {seed_text[:80]}...")
        
        source_code = call_openrouter(seed_text)
        if source_code:
            write_app(source_code, seed_id, seed_text)
            log(f"Successfully generated app for seed: {seed_text[:50]}...")
        else:
            # Fallback: create a placeholder
            log(f"Using fallback for seed: {seed_text[:50]}...")
            placeholder = f"""#!/usr/bin/env python3
# Generated placeholder for: {seed_text}
# This script could not be generated automatically.

def main():
    print("Seed topic: {seed_text[:200]}")

if __name__ == "__main__":
    main()
"""
            write_app(placeholder, seed_id, seed_text)
    
    log("Code gardener finished")

if __name__ == "__main__":
    main()
