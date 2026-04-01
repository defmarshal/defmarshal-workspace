#!/usr/bin/env python3
"""
Set up ChromaDB with initial documents:
- Research reports (research/*.md)
- OpenClaw documentation (MEMORY.md, AGENTS.md, CRON_JOBS.md)
- Code-gardener generated apps (apps/*.py)
"""

import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
DB_DIR = WORKSPACE / "data/chromadb"
DB_DIR.mkdir(parents=True, exist_ok=True)

# Use a small embedding model (all-MiniLM-L6-v2, ~80MB)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(
    name="openclaw_knowledge",
    embedding_function=embedding_func
)

# 1. Index OpenClaw docs
docs_to_index = []

# Add MEMORY.md summary
memory = WORKSPACE / "MEMORY.md"
if memory.exists():
    content = memory.read_text()
    docs_to_index.append({
        "id": "doc_memory",
        "text": content[:5000],  # limit size
        "metadata": {"source": "MEMORY.md", "type": "documentation"}
    })

# Add AGENTS.md
agents_doc = WORKSPACE / "AGENTS.md"
if agents_doc.exists():
    content = agents_doc.read_text()
    docs_to_index.append({
        "id": "doc_agents",
        "text": content[:5000],
        "metadata": {"source": "AGENTS.md", "type": "documentation"}
    })

# Add CRON_JOBS.md
cron_doc = WORKSPACE / "CRON_JOBS.md"
if cron_doc.exists():
    content = cron_doc.read_text()
    docs_to_index.append({
        "id": "doc_cron",
        "text": content[:5000],
        "metadata": {"source": "CRON_JOBS.md", "type": "documentation"}
    })

# 2. Index recent research reports (last 7 days)
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=7)
research_dir = WORKSPACE / "research"
if research_dir.exists():
    for md in research_dir.glob("*.md"):
        mtime = datetime.fromtimestamp(md.stat().st_mtime)
        if mtime >= cutoff:
            content = md.read_text()
            # Truncate to first 2000 chars for embedding
            docs_to_index.append({
                "id": f"research_{md.stem}",
                "text": content[:2000],
                "metadata": {"source": str(md.name), "type": "research", "date": mtime.isoformat()}
            })

# 3. Index code-gardener apps (last 10)
apps_dir = WORKSPACE / "apps"
if apps_dir.exists():
    apps = list(apps_dir.glob("*.py"))[-10:]  # last 10
    for app in apps:
        content = app.read_text()
        docs_to_index.append({
            "id": f"app_{app.stem}",
            "text": content[:2000],
            "metadata": {"source": str(app.name), "type": "code"}
        })

# Add to ChromaDB
if docs_to_index:
    collection.add(
        ids=[d["id"] for d in docs_to_index],
        documents=[d["text"] for d in docs_to_index],
        metadatas=[d["metadata"] for d in docs_to_index]
    )
    print(f"Indexed {len(docs_to_index)} documents into ChromaDB")
else:
    print("No documents found to index")

print(f"Collection count: {collection.count()}")
print(f"Database saved to {DB_DIR}")
