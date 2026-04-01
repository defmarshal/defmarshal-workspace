#!/usr/bin/env python3
"""
Extract chat history from OpenClaw memory logs and format for fine-tuning.
Outputs: data/personality.jsonl (ChatML format)
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Load recent memory logs to extract conversations
logs = list((WORKSPACE / "memory").glob("*.log"))
# Focus on recent logs where we chatted
recent_logs = sorted(logs, key=lambda x: x.stat().st_mtime, reverse=True)[:10]

def parse_conversation_lines(lines):
    """Extract user/assistant pairs from log lines."""
    conversations = []
    current = {"messages": []}
    for line in lines:
        # Look for "[USER]" or "[ASSISTANT]" markers, or def's messages
        if "defmarsh" in line or "Def M" in line:
            # Assume this is user message
            text = extract_message_text(line)
            if text:
                current["messages"].append({"role": "user", "content": text})
        elif "mewmew" in line or "me:" in line.lower():
            text = extract_message_text(line)
            if text:
                current["messages"].append({"role": "assistant", "content": text})
                # If we have both user+assistant, consider it a pair
                if len(current["messages"]) >= 2:
                    conversations.append(current.copy())
                    current = {"messages": []}
    return conversations

def extract_message_text(line):
    """Extract the actual message text, removing timestamps/prefixes."""
    # Simple: take everything after first ']' or ':' that looks like message
    parts = line.split("]", 1) if "]" in line else line.split(":", 1)
    if len(parts) > 1:
        text = parts[1].strip()
        # Skip empty or system messages
        if text and not text.startswith(("System:", "[", "(")):
            return text[:500]  # limit length
    return None

# Collect conversations
all_convos = []
for log in recent_logs:
    try:
        with open(log) as f:
            lines = f.readlines()
        convos = parse_conversation_lines(lines)
        all_convos.extend(convos)
    except Exception as e:
        print(f"Error reading {log}: {e}")

# Deduplicate and filter
seen = set()
unique_convos = []
for c in all_convos:
    # Create a simple hash of messages to dedup
    sig = "|".join(m["content"][:50] for m in c["messages"])
    if sig not in seen and len(c["messages"]) >= 2:
        seen.add(sig)
        unique_convos.append(c)

print(f"Found {len(unique_convos)} unique conversations")

# Add system prompt to each
for c in unique_convos:
    # Insert system message at beginning if not present
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
