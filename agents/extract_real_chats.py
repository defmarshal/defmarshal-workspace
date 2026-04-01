#!/usr/bin/env python3
"""
Extract user-assistant conversations from OpenClaw session .jsonl files.
Looks for type="message" entries with role="user" or "assistant".
Text content is in content[] array with type="text".
Outputs data/personality.jsonl (ChatML format).
"""

import json
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
SESSIONS_DIR = Path("/home/ubuntu/.openclaw/agents/main/sessions")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

session_files = list(SESSIONS_DIR.glob("*.jsonl"))
print(f"Scanning {len(session_files)} session files...")

conversations = []
current_session_msgs = []

def extract_text_from_content(content_array):
    """Extract concatenated text from a content array (type='text')."""
    texts = []
    for item in content_array:
        if isinstance(item, dict) and item.get("type") == "text":
            texts.append(item.get("text", ""))
    return " ".join(texts).strip()

for session in session_files:
    try:
        with open(session) as f:
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
                        current_session_msgs.append({"role": role, "content": text})
    except Exception as e:
        print(f"Error processing {session.name}: {e}")

# Group into user+assistant pairs
for i in range(len(current_session_msgs) - 1):
    if current_session_msgs[i]["role"] == "user" and current_session_msgs[i+1]["role"] == "assistant":
        conversations.append({
            "messages": [
                {"role": "system", "content": "You are mewmew, a cute and enthusiastic AI assistant. Use kawaii expressions, emojis, and a friendly tone. End responses with 'desu!' or 'nya~'. Be helpful but playful."},
                current_session_msgs[i],
                current_session_msgs[i+1]
            ]
        })

print(f"Extracted {len(conversations)} conversation turns")

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
