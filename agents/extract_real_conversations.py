#!/usr/bin/env python3
"""
Extract real chat conversations from memory/*.md files.
Looks for **USER**: and **ASSISTANT**: blocks (OpenClaw session transcripts).
Outputs data/personality.jsonl with ChatML format.
"""

import json
import re
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Scan all memory .md files
md_files = list((WORKSPACE / "memory").glob("*.md"))
print(f"Scanning {len(md_files)} memory .md files...")

conversations = []
current_msgs = []
in_transcript = False

def is_user_line(line):
    return re.search(r'\*\*USER\*\*:|^\[USER\]|^defmarshal:', line, re.IGNORECASE)

def is_assistant_line(line):
    return re.search(r'\*\*ASSISTANT\*\*:|^\[ASSISTANT\]|^mewmew:', line, re.IGNORECASE)

def extract_text(line):
    # Remove prefix like **USER**: or timestamps
    text = re.sub(r'^\*\*(USER|ASSISTANT)\*\*:\s*', '', line, flags=re.I)
    text = re.sub(r'^\[(USER|ASSISTANT)\]\s*', '', text, flags=re.I)
    text = re.sub(r'^defmarshal:\s*', '', text, flags=re.I)
    text = re.sub(r'^mewmew:\s*', '', text, flags=re.I)
    # Strip any leading timestamps like "( Wed 2026-04-01 07:25 GMT+7 )"
    text = re.sub(r'^\(.*?\)\s*', '', text)
    return text.strip()

for md in sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:30]:  # recent 30 files
    try:
        with open(md) as f:
            lines = f.readlines()
    except Exception as e:
        continue

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect transcript blocks
        if "**USER**:" in line or "**ASSISTANT**:" in line:
            in_transcript = True
        elif in_transcript and any(marker in line for marker in ["System:", "---", "##", "SESSION"]):
            # End of transcript block
            if len(current_msgs) >= 2:
                # Take last user+assistant pair as one exchange
                conversations.append({"messages": current_msgs[-2:]})
            current_msgs = []
            in_transcript = False
            continue

        if not in_transcript:
            continue

        if is_user_line(line):
            text = extract_text(line)
            if text and len(text) > 2:
                current_msgs.append({"role": "user", "content": text})
        elif is_assistant_line(line):
            text = extract_text(line)
            if text and len(text) > 2:
                current_msgs.append({"role": "assistant", "content": text})
                # If we have at least one user+assistant, capture the exchange
                roles = [m["role"] for m in current_msgs]
                if "user" in roles and "assistant" in roles:
                    # Keep sliding window of last 2 messages
                    if len(current_msgs) > 2:
                        current_msgs = current_msgs[-2:]

# Final flush
if len(current_msgs) >= 2:
    conversations.append({"messages": current_msgs[-2:]})

# Deduplicate
seen = set()
unique_convos = []
for c in conversations:
    sig = "|".join(m["content"][:60] for m in c["messages"])
    if sig not in seen and len(c["messages"]) >= 2:
        seen.add(sig)
        unique_convos.append(c)

print(f"Extracted {len(unique_convos)} conversations")

# Add system prompt
for c in unique_convos:
    if not any(m.get("role") == "system" for m in c["messages"]):
        c["messages"].insert(0, {
            "role": "system",
            "content": "You are mewmew, a cute and enthusiastic AI assistant. Use kawaii expressions, emojis, and a friendly tone. End responses with 'desu!' or 'nya~'. Be helpful but playful."
        })

# Write JSONL
with open(OUTPUT, "w") as f:
    for c in unique_convos:
        f.write(json.dumps({"messages": c["messages"]}) + "\n")

print(f"Wrote {len(unique_convos)} examples to {OUTPUT}")
