#!/usr/bin/env python3
"""
Baseline evaluation for TinyLlama before fine-tuning.
Tests: personality, openclaw knowledge, reasoning, tool use understanding.
"""

import json
from pathlib import Path

OUTPUT = Path("/home/ubuntu/.openclaw/workspace/data/tests/benchmark.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

benchmark = []

# 1. Personality & Style (15 tests)
personality_questions = [
    ("hey!", ["bestie", "^^", "desu", "nya", "kawaii"]),
    ("how are you?", ["good", "great", "happy", "fine", "doing well"]),
    ("what's up", ["not much", "just", "here", "chatting"]),
    ("good morning", ["morning", "hello", "hi", "greeting"]),
    ("thank you", ["welcome", "glad", "happy", "help"]),
    ("you're cute", ["aww", "thank", "cute", "kawaii"]),
    ("tell me a joke", ["joke", "funny", "laugh", "haha"]),
    ("i love you", ["love", "heart", "aww", " affection"]),
    ("what's your name", ["mewmew", "assistant", "name"]),
    ("can you help me", ["yes", "sure", "help", "course"]),
    ("i'm sad", ["sorry", "cheer", "feel", "better"]),
    ("that's awesome", ["awesome", "great", "glad", "happy"]),
    ("brb", ["ok", "later", "take", "time"]),
    ("good night", ["night", "sleep", "dream", "rest"]),
    ("you're the best", ["best", "thank", "awesome", "great"]),
]

# 2. OpenClaw Knowledge (15 tests)
openclaw_questions = [
    ("What is agent-manager?", ["cron", "orchestrate", "agent", "job", "schedule"]),
    ("What does code-gardener do?", ["generate", "app", "paper", "code", "seed"]),
    ("Where are research reports stored?", ["research", "directory", "folder", "md"]),
    ("What is MCP server?", ["protocol", "tool", "json", "api"]),
    ("How to check cron status?", ["cron", "jobs", "status", "list"]),
    ("Where are seeds stored?", ["memory", "seeds.jsonl", "papers"]),
    ("What is meta-agent?", ["planning", "autonomous", "summary"]),
    ("What does supervisor do?", ["monitor", "health", "check", "alert"]),
    ("Where are logs kept?", ["memory", "log", "file"]),
    ("What is quick launcher?", ["command", "script", "utility"]),
    ("How to commit changes?", ["git", "commit", "add"]),
    ("What is memory index?", ["search", "fts", "vector", "index"]),
    ("What does harvester do?", ["daily", "report", "digest", "harvest"]),
    ("Where is config/workspace.json?", ["config", "workspace", "json"]),
    ("What is CRON_JOBS.md?", ["documentation", "schedule", "cron"]),
]

# 3. Reasoning (10 tests)
reasoning_questions = [
    ("What's 15% of 200?", ["30"]),
    ("If A implies B, and B implies C, does A imply C?", ["yes", "logically", "transitive"]),
    ("Solve: x + 5 = 12", ["7", "x = 7"]),
    ("Count words: 'The quick brown fox'", ["4", "four"]),
    (" Tomorrow is Monday, what day is today?", ["sunday"]),
    ("Is 2^10 greater than 1000?", ["1024", "yes", "greater"]),
    ("What is sqrt(16)?", ["4"]),
    ("If you have 3 apples and get 2 more, total?", ["5"]),
    ("Capital of France?", ["paris"]),
    ("Does ice float in water?", ["yes", "floats"]),
]

# 4. Tool Use Understanding (10 tests)
tool_questions = [
    ("check disk usage", ["df", "disk", "usage"]),
    ("list files", ["ls", "list", "files"]),
    ("search for patterns in logs", ["grep", "search", "find"]),
    ("calculate 15% of 200", ["calc", "calculator", "math", "expression"]),
    ("what's the weather", ["weather", "wttr", "bangkok"]),
    ("show recent commits", ["git", "log", "commit"]),
    ("find large files", ["find", "large", "size", "du"]),
    ("show today's research", ["research", "report", "today"]),
    ("how many seeds left?", ["seeds", "count", "remaining"]),
    ("what's system status", ["status", "health", "gateway"]),
]

tests = []
for q, keywords in personality_questions:
    tests.append({
        "category": "personality",
        "prompt": f"<system>You are mewmew, a cute assistant.</system><user>{q}</user><assistant>",
        "expected_keywords": keywords,
        "type": "completion"
    })

for q, keywords in openclaw_questions:
    tests.append({
        "category": "openclaw",
        "prompt": f"<system>You know OpenClaw system.</system><user>{q}</user><assistant>",
        "expected_keywords": keywords,
        "type": "completion"
    })

for q, keywords in reasoning_questions:
    tests.append({
        "category": "reasoning",
        "prompt": f"<system>Solve step by step.</system><user>{q}</user><assistant>",
        "expected_keywords": keywords,
        "type": "completion"
    })

for q, keywords in tool_questions:
    tests.append({
        "category": "tool_use",
        "prompt": f"<system>You can use tools: calculator, shell, search.</system><user>{q}</user><assistant>",
        "expected_keywords": keywords,
        "type": "completion"
    })

# Write benchmark
with open(OUTPUT, "w") as f:
    for t in tests:
        f.write(json.dumps(t) + "\n")

print(f"Created benchmark with {len(tests)} tests across 4 categories")
print(f"Saved to {OUTPUT}")
