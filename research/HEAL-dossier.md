# HEAL Research Dossier

**Paper:** Hindsight Entropy-Assisted Learning for Reasoning Distillation (arXiv:2603.10359v1)
**Date:** 2026-03-13
**Status:** Deep research completed, ready for implementation planning

---

## 1. Problem & Real-World Impact

**Problem:** Distilling reasoning capabilities from large teacher models into smaller student models via standard SFT is inefficient; it misses hard but valuable reasoning trajectories, leading to a "teacher ceiling".

**Impact:** Better distillation enables smaller, cheaper models with teacher-level reasoning — deployable on edge devices, lower inference cost, broader accessibility.

---

## 2. Core Insight & Novelty

**HEAL** combines three innovations:

- **GEAR**: Entropy-guided local repair of failing reasoning paths.
- **PURE**: Quality filter to remove spurious trajectories (shortcuts).
- **PACE**: Three-stage curriculum (base → hint → repair) for stable training.

Together they yield ~10% absolute accuracy gain on challenging math benchmarks.

---

## 3. Methodology Deep Dive

### 3.1. GEAR (Guided Entropy-Assisted Repair)

- Sample 30 trajectories per problem from teacher.
- Compute entropy dynamics to find reasoning dead-ends.
- Identify breakpoint (max entropy surge in first third).
- Backup one step and generate answer-conditioned hint.
- For extremely hard problems (≤1 correct in 30), select 10 incorrect paths and repair each, generating 20 repaired candidates per path.

### 3.2. PURE (Perplexity-Uncertainty Ratio Estimator)

- Segment trajectories into steps (`\n\n` delimiter).
- Compute ratio of step perplexity to answer uncertainty.
- Filter out high-anomaly (spurious) trajectories.
- Hyperparameters: λ=0.2, ε=0.01.

### 3.3. PACE (Progressive Answer-guided Curriculum Evolution)

- **Stage I (Base)**: 30 samples per problem.
- **Stage II (Hint)**: Add answer-guided samples for hard problems (Pass@30 < 0.5).
- **Stage III (Repair)**: Add GEAR-repaired samples for extremely hard problems.

Training: 5 epochs, LR=1e-5, batch size 8, 8×H100 GPUs (we'll scale).

---

## 4. Feasibility Assessment

**Feasible with modest scaling:**
- Use smaller models: teacher = Qwen2.5-7B, student = Qwen2.5-1.5B or 3B.
- Use dataset subset (100–200 AIME problems) to reduce compute.
- Implement on single GPU (or CPU with LoRA if needed).
- Expected training time: several hours to a day per experiment.

**Risks:** Model access, compute speed, implementation complexity. Mitigation: use open models, start with tiny scale.

---

## 5. Existing Implementations

None — this is bleeding edge. We will build from scratch based on the LaTeX paper.

---

## 6. Success Criteria

1. **Replication** on small scale: produce working HEAL pipeline.
2. **Measurable improvement**: HEAL student outperforms SFT baseline by ≥5% absolute on held-out set.
3. **Usable artifact**: Installable Python package (`heal-distill`) with API, examples, docs.
4. **Evaluation report**: Markdown with results, ablations, analysis.

---

## 7. Risks & Mitigations

See dossier above.

---

## 8. Resource Estimate

- Compute: ~20–50 GPU-hours (scaled down); can be done sequentially.
- Storage: <10GB.
- Dev-agent cycles: Estimated 30–50 cycles for implementation + testing.

---

## 9. Recommendation

**Greenlight.** Proceed with MVP implementation using scaled-down models/dataset. Target 2 weeks for first working version.
