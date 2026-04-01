#!/usr/bin/env python3
"""
Extract ALL user-assistant conversations from ALL agent session directories.
"""

import json
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
AGENTS_DIR = Path("/home/ubuntu/.openclaw/agents")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Find all agent session directories
session_dirs = list(AGENTS_DIR.glob("*/sessions"))
print(f"Found {len(session_dirs)} agent session directories")

conversations = []

def extract_text_from_content(content_array):
    texts = []
    for item in content_array:
        if isinstance(item, dict) and item.get("type") == "text":
            texts.append(item.get("text", ""))
    return " ".join(texts).strip()

total_sessions = 0
for session_dir in session_dirs:
    session_files = list(session_dir.glob("*.jsonl"))
    total_sessions += len(session_files)

    for session in session_files:
        try:
            with open(session) as f:
                msgs = []
                for line in f:
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if entry.get("type") != "message":
                        continue

                    msg_obj = entry.get("message", {})
                    role = msg_obj.get("role")
                    content_array = msg_obj.get("content", [])

                    if role in ("user", "assistant"):
                        text = extract_text_from_content(content_array)
                        if text and len(text) > 5:
                            msgs.append({"role": role, "content": text})

                # Pair ALL consecutive user+assistant messages
                i = 0
                while i < len(msgs) - 1:
                    if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant":
                        conversations.append({
                            "messages": [
                                {"role": "system", "content": "You are mewmew, a cute and enthusiastic AI assistant. Use kawaii expressions, emojis, and a friendly tone. End responses with 'desu!' or 'nya~'. Be helpful but playful."},
                                msgs[i],
                                msgs[i+1]
                            ]
                        })
                        i += 2
                    else:
                        i += 1
        except Exception as e:
            print(f"Error in {session}: {e}")

print(f"Scanned {total_sessions} sessions")
print(f"Extracted {len(conversations)} conversation turns (raw)")

# Deduplicate
seen = set()
unique_convos = []
for c in conversations:
    sig = "|".join(m["content"][:100] for m in c["messages"] if m["role"] != "system")
    if sig not in seen:
        seen.add(sig)
        unique_convos.append(c)

print(f"After dedup: {len(unique_convos)} unique conversations")

# Write JSONL
with open(OUTPUT, "w") as f:
    for c in unique_convos:
        f.write(json.dumps({"messages": c["messages"]}) + "\n")

print(f"✅ Wrote {len(unique_convos)} examples to {OUTPUT}")
