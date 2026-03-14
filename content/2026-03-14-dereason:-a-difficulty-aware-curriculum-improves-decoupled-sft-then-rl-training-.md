# DeReason: A Difficulty-Aware Curriculum Improves Decoupled SFT-then-RL Training for General Reasoning

*What if you could teach an AI to think better by giving it the right problems at the right time? A clever new curriculum splits training data by difficulty, and the results are impressive.*

---

## Introduction: The SFT vs. RL Tug-of-War

Reinforcement Learning with Verifiable Rewards (RLVR) has been the star of recent AI reasoning breakthroughs—think OpenAI's o1 and DeepSeek-R1. By rewarding models for correct answers in math and coding, RLVR unlocks sophisticated chain-of-thought reasoning, self-verification, and reflection.

But here's the catch: RLVR's magic works best in narrow domains with clear right/wrong answers. When you move to general STEM questions—biology, physics, interdisciplinary problems—RLVR becomes **sample-inefficient** and often gets outperformed by good old **supervised fine-tuning (SFT)** on moderate-quality responses.

So which is better? The answer is: **both**, but you have to use them the right way. DeReason, a new difficulty-aware curriculum, shows that splitting training data by reasoning intensity yields significantly better results than any pure approach or random split. It's not just "SFT then RL"—it's "*the right data for the right stage*."

---

## Key Insights

### 🔍 The Critical Discovery: SFT Beats RL on General STEM

Controlled experiments revealed a surprising division of labor:
- **Pure RLVR** on base models is highly sample-inefficient for general reasoning.
- **SFT** on moderate-quality responses consistently outperforms RLVR in these broader domains.
- However, **sequential SFT-then-RL** can further improve performance, suggesting the two stages are complementary—not competing.

The key question becomes: *How should we allocate data between SFT and RL?*

---

### 📊 DeReason's Clever Partition: Difficulty-Based Data Decoupling

DeReason introduces **reasoning intensity** as the partitioning criterion. Using an LLM scorer, each training problem gets a score from 1 to 5:

- **Low reasoning intensity** (1–2): knowledge recall, straightforward application of facts.
- **High reasoning intensity** (4–5): multi-step derivation, complex inference, synthesis across concepts.

Then:
- **SFT** gets the *broad-coverage, non-reasoning-intensive* problems → establishes foundational domain knowledge efficiently via knowledge distillation.
- **RL** gets the *focused, difficult* problems → cultivates advanced reasoning by exploring beyond teacher demonstrations.

This matches each stage's strength: SFT excels at teaching known patterns; RL excels at searching for novel, high-reward reasoning paths.

---

### 🏆 Results: Decoupled Curriculum Dominates

Experiments across general STEM and mathematical benchmarks show:

- **DeReason significantly outperforms:**
  - SFT-only
  - RL-only
  - Random SFT-then-RL splits

The gains are substantial and consistent across model sizes and datasets. Notably, this approach works well even for smaller models where pure RLVR struggles.

---

### 🧠 Why This Works: Complementary Roles

- **SFT** provides a cold-start and distills broad knowledge from a stronger teacher model. It's efficient for covering the "long tail" of factual recall and standard problem patterns.
- **RLVR** then fine-tunes the model to explore more creative, multi-step reasoning on hard problems where the teacher's answer may not be the only (or best) path. RL's reward signal encourages the model to go beyond imitation.

By **decoupling** the data, you avoid forcing RL to waste time on easy problems it's bad at, and you avoid using SFT to try to teach complex reasoning (which it can only parrotingly imitate).

---

## Why This Matters for AI Training

DeReason offers a **practical, generalizable recipe** for post-training LLMs on reasoning tasks beyond narrow math/code:

- **No algorithmic changes** – just smarter data selection. Orthogonal to other RL/SFT improvements.
- **Scales to general STEM** – works across biology, physics, interdisciplinary questions.
- **Efficient** – RL portion focuses on hard problems where it actually adds value.
- **Easy to implement** – score data with an LLM, split by threshold, train sequentially.

For organizations building reasoning models, this means you can get better performance without changing your training toolkit—just curate data more thoughtfully.

---

## Conclusion: Match the Method to the Problem

The debate between SFT and RLVR has often been framed as a winner-takes-all contest. DeReason shows that's the wrong framing. The real insight is that **different training stages serve different purposes**, and you should allocate your data accordingly.

Teach the basics with SFT (knowledge distillation). Challenge the hard stuff with RL (exploration). Don't make RL learn what it's bad at, and don't use SFT to try to cultivate genuine reasoning. A difficulty-aware curriculum aligns the training method with the nature of the problem.

The result? Better reasoning, more efficient training, and a clear blueprint for post-training that generalizes beyond math to the full spectrum of STEM intelligence.

---

*Based on: Hu, H. et al. (2026). "DeReason: A Difficulty-Aware Curriculum Improves Decoupled SFT-then-RL Training for General Reasoning." arXiv:2603.11193v1. 13 pages, 6 figures.*