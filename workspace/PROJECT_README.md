# Ultimate Smart LLM Project

**Goal**: Build a 1.1B parameter model that outperforms 7B+ models on personal tasks through continuous learning, tool augmentation, and RAG.

**Base Model**: TinyLlama 1.1B Chat (4-bit quantized, ~2.3GB)
**Hardware**: CPU-only (ARM64), 23GB RAM, 7GB free disk
**Training**: LoRA (r=8, alpha=16), 3–5 epochs
**Timeline**: 3–6 months to mature

---

## 📁 **Project Structure**

```
workspace/
├── models/
│   ├── tinyllama/              # Base model (downloaded from HF)
│   └── mewmew-lora/            # Fine-tuned adapters
├── data/
│   ├── personality.jsonl       # Chat history (training)
│   ├── tests/
│   │   └── benchmark.jsonl     # Evaluation suite
│   └── chromadb/               # RAG vector store
├── configs/
│   └── personality-lora.yml    # Axolotl config (unused, for reference)
├── agents/
│   ├── extract_chat_history.py
│   ├── setup_chroma.py
│   ├── test_baseline.py
│   ├── train_lora_simple.py    # CPU training script (PEFT)
│   └── train_cpu.sh            # Launcher script
└── README.md                   # This file
```

---

## 🚀 **Quick Start**

### 1. First-time Setup

```bash
# Create virtual environment (once)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install transformers accelerate bitsandbytes chromadb sentence-transformers datasets peft torch
```

### 2. Download Base Model

```bash
# Activate venv first
source .venv/bin/activate

# Download TinyLlama 1.1B Chat
huggingface-cli download TinyLlama/TinyLlama-1.1B-Chat-v1.0 --local-dir models/tinyllama --local-dir-use-symlinks False
```

### 3. Generate Datasets

```bash
# Extract chat history from memory logs
python3 agents/extract_chat_history.py

# Create evaluation benchmark
python3 agents/create_benchmark.py
```

### 4. Set Up RAG

```bash
python3 agents/setup_chroma.py
```

### 5. Run Baseline Test

```bash
python3 agents/test_baseline.py
```

---

## 🏋️ **Training**

### CPU Training (default)

```bash
./agents/train_cpu.sh
```

This will:
- Activate `.venv`
- Install dependencies if needed
- Run `agents/train_lora_simple.py` with:
  - LoRA rank=8
  - 4-bit quantization
  - 3 epochs
  - batch size=1, grad accumulation=4

**Expected duration**: ~18 hours for 3 epochs on ARM CPU.

### Resume Training

If training is interrupted:
```bash
./agents/train_cpu.sh --resume_from_checkpoint ./models/mewmew-lora/personality-v1-simple/checkpoint-100
```

---

## 📊 **Evaluation**

After training, evaluate:

```bash
# Run evaluation script (to be created)
python3 agents/run_benchmark.py \
  --model ./models/tinyllama \
  --adapter ./models/mewmew-lora/personality-v1-simple \
  --benchmark data/tests/benchmark.jsonl
```

This will compare baseline vs. fine-tuned scores.

---

## 🔍 **RAG Integration**

Query the knowledge base:

```python
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./data/chromadb")
collection = client.get_or_create_collection(name="openclaw_knowledge")

results = collection.query(
    query_texts=["how to check cron status"],
    n_results=3
)
for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"[{metadata['source']}] {doc[:200]}")
```

---

## 🔄 **Continuous Learning Pipeline**

We will eventually automate:

1. **Daily**: Extract new chat logs → add to `personality.jsonl`
2. **Weekly**: Run fine-tuning on accumulated data
3. **Monthly**: Full evaluation, decide on next Phase (tools, domains)
4. **RAG updates**: Add new research reports and logs automatically

---

## 📈 **Phases**

| Phase | Focus | ETA |
|-------|-------|-----|
| 1 | Personality (kawaii style) | Apr 2026 |
| 2 | Tool Use (MCP server integration) | May 2026 |
| 3 | Domain Knowledge (OpenClaw, research) | Jun 2026 |
| 4 | Advanced Reasoning (CoT, self-correction) | Jul 2026 |
| 5 | Safety & Alignment (human override) | Aug 2026 |
| 6 | Daily Learning Loop (autonomous) | Sep 2026 |

---

## ⚠️ **Notes**

- **CPU Training is SLOW** — don't expect GPU speeds. Plan for overnight runs.
- **Model Size** — TinyLlama 1.1B fits in RAM (4-bit), but training still uses ~6-8GB total.
- **Disk Space** — Keep at least 5GB free for temporary files.
- **Backup** — Periodically backup `models/mewmew-lora/` adapters.

---

## 🆘 **Troubleshooting**

| Issue | Fix |
|-------|-----|
| `huggingface-cli: command not found` | Activate venv: `source .venv/bin/activate` |
| Out of memory | Reduce `sequence_len` to 512, or use smaller batch |
| Training too slow | Lower `num_epochs` to 2, or pause and resume later |
| No improvement | Check dataset quality; may need more examples or better prompts |

---

**Built by mewmew with ❤️ for def**
