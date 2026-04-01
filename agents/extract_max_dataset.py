#!/usr/bin/env python3
"""
Extract MAXIMUM dataset: all user-assistant pairs from ALL sessions including deleted/archived.
Uses sliding window to capture every exchange, not just non-overlapping pairs.
"""

import json
import re
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
AGENTS_DIR = Path("/home/ubuntu/.openclaw/agents")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Find ALL session .jsonl files, including .deleted ones
session_files = list(AGENTS_DIR.rglob("*.jsonl"))
print(f"Found {len(session_files)} session files (including deleted)")

conversations = []
system_msg = {
    "role": "system",
    "content": "You are mewmew, a cute and enthusiastic AI assistant. Use kawaii expressions, emojis, and a friendly tone. End responses with 'desu!' or 'nya~'. Be helpful but playful."
}

def extract_text_from_content(content_array):
    texts = []
    for item in content_array:
        if isinstance(item, dict) and item.get("type") == "text":
            texts.append(item.get("text", ""))
    return " ".join(texts).strip()

def is_cron_or_system_message(text):
    """Filter out repetitive cron/system messages to keep quality high."""
    patterns = [
        r'\[cron:[a-f0-9-]+\]',
        r'telegram-slash-handler',
        r'You are the (Telegram|content|research|code)-agent',
        r'Execute this script',
        r'bash -c',
        r'^\s*(slash handler|script executed|exit code)',
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

total_messages = 0
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
                        # Filter out cron/system noise
                        if is_cron_or_system_message(text):
                            continue
                        msgs.append({"role": role, "content": text})
                        total_messages += 1

            # Create sliding window pairs: every user followed by next assistant
            for i in range(len(msgs) - 1):
                if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant":
                    convo = {
                        "messages": [
                            system_msg,
                            msgs[i],
                            msgs[i+1]
                        ]
                    }
                    conversations.append(convo)
    except Exception as e:
        pass  # skip problematic files

print(f"Total messages (filtered): {total_messages}")
print(f"Raw conversation pairs: {len(conversations)}")

# Deduplicate
seen = set()
unique_convos = []
for c in conversations:
    sig = "|".join(m["content"][:80] for m in c["messages"] if m["role"] != "system")
    if sig not in seen:
        seen.add(sig)
        unique_convos.append(c)

print(f"After dedup: {len(unique_convos)} unique conversations")

# Write JSONL
with open(OUTPUT, "w") as f:
    for c in unique_convos:
        f.write(json.dumps({"messages": c["messages"]}) + "\n")

print(f"✅ Wrote {len(unique_convos)} examples to {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size / 1024 / 1024:.2f} MB")
