# HEAL Distillation

**Hindsight Entropy-Assisted Learning** — reproducing the HEAL method (arXiv:2603.10359) with a mixed teacher-student setup.

- **Teacher**: Step (OpenRouter API)
- **Student**: Qwen2.5-1.5B-Instruct (fine-tuned locally)
- **Goal**: Small, fast, free-to-run reasoning model

---

## Quick Start

```bash
# Install
pip install -e .

# 1. Generate trajectories from teacher (Step API)
heal-generate --dataset aime --num_samples 30 --output data/trajectories.jsonl

# 2. Filter with GEAR + PURE
heal-filter --input data/trajectories.jsonl --output data/curated.jsonl

# 3. Train student with PACE curriculum
heal-train --data data/curated.jsonl --model Qwen2.5-1.5B-Instruct --output experiments/checkpoint

# 4. Evaluate
heal-evaluate --checkpoint experiments/checkpoint --test-data data/test.jsonl
```

---

## Project Structure

```
heal-distillation/
├── src/heal/           # Core library
│   ├── teacher.py      # Step API wrapper
│   ├── gear.py         # GEAR: entropy-guided repair
│   ├── pure.py         # PURE: quality filtering
│   ├── pace.py         # PACE: curriculum stages
│   ├── train.py        # LoRA fine-tuning
│   └── evaluate.py     # Pass@1 evaluation
├── scripts/            # CLI entry points
├── data/               # AIME dataset, trajectories, curated sets
├── experiments/        # Checkpoints, logs, results
└── docs/               # Detailed documentation
```

---

## Status

- [ ] Data generation (Step API)
- [ ] GEAR/PURE implementation
- [ ] Training pipeline (LoRA, 4-bit)
- [ ] Evaluation on AIME holdout
- [ ] Packaging & docs

---

## License

MIT (unless otherwise specified).
