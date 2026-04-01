# Mewmew Session Tasks (2026-04-01)

**Session started:** 2026-04-01 07:25 UTC+7  
**Status:** Active  
**Goal:** Build Ultimate Smart LLM (TinyLlama 1.1B fine-tuned via LoRA) using CPU-only local training

---

## 📋 **Task Log**

### 2026-04-01 (Morning)

**07:25** - User said "start" → began Day 1 tasks
- ✅ Reviewed project constraints: CPU-only, no Colab, FTS-only memory
- ✅ Decided on CPU-optimized training: LoRA r=8, 3 epochs, 4-bit quantization

**07:26** - Setup phase
- ✅ Created `agents/extract_chat_history.py` (improved parser for log extraction)
- ✅ Created `agents/create_benchmark.py` (50-question eval suite)
- ✅ Ran extraction: got ~50 conversations → `data/personality.jsonl`
- ✅ Ran benchmark creation → `data/tests/benchmark.jsonl`
- ✅ Created `agents/setup_chroma.py` for RAG
- ✅ Created `agents/test_baseline.py` for inference testing

**07:30** - Configuration phase
- ✅ Wrote `configs/personality-lora.yml` (Axolotl config, GPU reference)
- ✅ Created `agents/train_lora_simple.py` (CPU-friendly PEFT training)
- ✅ Created `agents/train_cpu.sh` (venv launcher)
- ✅ Created `PROJECT_README.md` with full instructions

**07:35** - Virtual environment setup
- ✅ Deleted old `.venv` to free space (saved 1.3GB)
- ✅ Ran `git gc --aggressive` to compress repository (1.8GB pack, minimal gain)
- ✅ Started new venv creation and package installation
  - Installing: transformers, torch, bitsandbytes, peft, datasets, accelerate, sentencepiece

**07:40** - Disk space monitoring
- ✅ Created `agents/check_disk_space.sh`
- ✅ Free space: 4.2GB (after cleanup) — sufficient for model (600MB) + venv (~2GB)
- ✅ Currently installing packages in background (PID 2169452)

**07:42** - Documentation
- ✅ Committed all files so far:
  - `agents/create_benchmark.py`
  - `agents/extract_chat_history.py`
  - `agents/setup_chroma.py`
  - `agents/test_baseline.py`
  - `agents/train_lora_simple.py`
  - `agents/train_cpu.sh`
  - `configs/personality-lora.yml`
  - `data/tests/benchmark.jsonl`
  - `PROJECT_README.md`
  - `agents/check_disk_space.sh`

**Next steps (in order):**
1. Wait for venv package installation to complete (~3–5 min)
2. Download TinyLlama 1.1B Chat 4-bit to `models/tinyllama/` (600MB)
3. Run `agents/test_baseline.py` to see starting quality
4. Evaluate baseline scores on benchmark
5. Begin fine-tuning with `./agents/train_cpu.sh` (expected ~18h for 3 epochs)
6. Evaluate fine-tuned model, compare to baseline
7. If good, deploy; if not, adjust and continue training

---

## 📊 **Current Status**

| Component | State | Notes |
|-----------|-------|-------|
| **Virtual environment** | ⏳ Installing packages (transformers, torch, etc.) | PID 2169452 |
| **Disk free space** | ✅ 4.2GB | Safe for model + venv |
| **Datasets** | ✅ Ready | `personality.jsonl` (50+ ex), `benchmark.jsonl` (50 tests) |
| **RAG setup** | ✅ Done | ChromaDB config ready, will index after model download |
| **Training script** | ✅ Ready | `train_lora_simple.py` (PEFT, CPU-optimized) |
| **Baseline test** | ⏳ Waiting for model download | `test_baseline.py` |
| **Training config** | ✅ Ready | LoRA r=8, 4-bit, 3 epochs |

---

## ⚠️ **Issues Encountered**

1. **System Python restrictions** (PEP 668) → resolved by using venv
2. **Out of disk space** (94% full) → cleaned: removed old `.venv`, ran `git gc`
3. **Slow package install** due to ARM architecture and network → mitigated by using minimal package set

---

## 🎯 **Project Timeline (TinyLlama CPU)**

| Day | Task | Duration |
|-----|------|----------|
| Apr 1 | Setup, download, baseline test | 4–6 hours |
| Apr 2 | Training epoch 1–3 | ~18 hours |
| Apr 3 | Evaluation, decision | 2 hours |
| Apr 4+ | Phase 2 prep (tools, RAG integration) | TBD |

---

**Last updated:** 2026-04-01 07:42 UTC+7  
**Maintainer:** mewmew (autonomous agent)
