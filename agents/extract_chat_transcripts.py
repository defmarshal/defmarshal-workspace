#!/usr/bin/env python3
"""
Extract conversations from memory/*.md chat transcript files.
Looks for 'assistant:' and 'user:' lines in session logs.
Outputs data/personality.jsonl (ChatML format).
"""

import json
import re
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
OUTPUT = WORKSPACE / "data/personality.jsonl"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Scan memory .md files that look like chat transcripts
md_files = list((WORKSPACE / "memory").glob("*.md"))
# Prioritize files with timestamps in name (likely session logs)
recent_files = sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:50]

conversations = []
current_exchange = []

def is_chat_line(line):
    """Check if line starts a user or assistant message."""
    return re.match(r'^(user|assistant):\s+', line, re.IGNORECASE)

def extract_role_and_text(line):
    """Extract role and message text from a chat line."""
    match = re.match(r'^(user|assistant):\s+(.+)$', line, re.IGNORECASE)
    if match:
        role = "user" if match.group(1).lower() == "user" else "assistant"
        text = match.group(2).strip()
        return role, text
    return None, None

for md in recent_files:
    try:
        with open(md) as f:
            lines = f.readlines()
    except Exception:
        continue

    in_chat_block = False
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip the header/metadata section at the start
        if line.startswith("---") or line.startswith("# Session"):
            in_chat_block = True  # assume after first marker we're in chat
            continue

        if not in_chat_block:
            continue

        # Check for conversation info or other non-chat sections
        if line.startswith("## ") or line.startswith("**") and ("**" in line[2:]):
            # Likely a heading or summary — reset
            if current_exchange:
                if len(current_exchange) >= 2:
                    conversations.append({"messages": current_exchange.copy()})
                current_exchange = []
            continue

        if is_chat_line(line):
            role, text = extract_role_and_text(line)
            if role and text and len(text) > 2:
                current_exchange.append({"role": role, "content": text})
                # Keep only last user+assistant pair to avoid context bleed
                if len(current_exchange) > 2:
                    current_exchange = current_exchange[-2:]

# Final flush
if len(current_exchange) >= 2:
    conversations.append({"messages": current_exchange.copy()})

# Deduplicate
seen = set()
unique_convos = []
for c in conversations:
    # Only keep if we have both user and assistant
    roles = [m["role"] for m in c["messages"]]
    if "user" not in roles or "assistant" not in roles:
        continue
    # Create signature
    sig = "|".join(m["content"][:80] for m in c["messages"])
    if sig not in seen:
        seen.add(sig)
        unique_convos.append(c)

print(f"Found {len(unique_convos)} chat exchanges")

# Add system prompt to each
system_msg = {
    "role": "system",
    "content": "You are mewmew, a cute and enthusiastic AI assistant. Use kawaii expressions, emojis, and a friendly tone. End responses with 'desu!' or 'nya~'. Be helpful but playful."
}
for c in unique_convos:
    if not any(m.get("role") == "system" for m in c["messages"]):
        c["messages"].insert(0, system_msg)

# Write JSONL
with open(OUTPUT, "w") as f:
    for c in unique_convos:
        f.write(json.dumps({"messages": c["messages"]}) + "\n")

print(f"Wrote {len(unique_convos)} examples to {OUTPUT}")
