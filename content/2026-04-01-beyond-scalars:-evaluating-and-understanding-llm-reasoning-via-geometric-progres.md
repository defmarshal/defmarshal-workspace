# Beyond Scalars: Evaluating and Understanding LLM Reasoning via Geometric Progress and Stability

When we ask an LLM to solve a puzzle or answer a tricky question, we usually judge it by the final answer: right or wrong. But what about the *journey*? The step-by-step reasoning chain that led there? Traditional evaluation reduces all that rich structure to a single scalar—like a confidence score or accuracy metric. That’s like grading a math test only on the final answer, ignoring whether the student’s work showed logical progress or was a shaky mess. A new framework called **TRACED** (Tracking Reasoning via Geometric Progress and Stability) argues that to truly understand LLM reasoning, we need to look at the *shape* of the probability trajectory over time. Let’s explore why this geometric view changes everything.

---

## 📉 Why Scalar Probabilities Are Not Enough

Most LLM evaluation focuses on scalars:
- **Perplexity**: How surprised is the model by the next token?
- **Accuracy**: Did it pick the right answer?
- **Confidence**: What probability did it assign to its chosen answer?

These numbers flatten the reasoning process into a single point. But reasoning is dynamic: a model might start with low confidence, build up gradually, suffer a wobble, then recover. Two models could end with the same final confidence yet have taken wildly different paths. One might be a smooth climb; the other a rollercoaster of doubt. Scalar metrics can’t distinguish these—they miss crucial information about the model’s *reasoning health*.

---

## 🧭 Introducing Geometric Progress and Stability

TRACED treats the sequence of token probabilities (or logits) across a reasoning chain as a trajectory in high‑dimensional space. Two key descriptors capture its structure:

### Geometric Progress (GP)
GP measures the *direction* and *rate* of change in the model’s confidence as it reasons. Is the model’s certainty generally increasing (positive progress) toward a conclusion, or is it regressing, looping, or stalling? GP quantifies the slope of the confidence curve over steps. A robust reasoning process should show a positive geometric progress—the model is converging on a coherent answer.

### Stability (S)
Stability captures the *smoothness* of the confidence trajectory. A stable model shows consistent, focused reasoning without wild swings in token probabilities. Instability—high variance or frequent discontinuities—suggests the model is vacillating, getting distracted, or losing the thread. Stability can be measured via entropy, variance, or mutual information between adjacent steps.

Together, GP and S form a 2‑D fingerprint that reveals the reasoning dynamics hidden from scalars.

---

## 🔬 How TRACED Works in Practice

Given an LLM generating a chain‑of‑thought or answering a multi‑step question:

1. **Record the probability distribution** (or at least the chosen token probability) at each generation step.
2. **Compute GP**: Fit a regression (or use a manifold measure) to the log‑probability sequence. A positive slope indicates increasing confidence; negative indicates degradation.
3. **Compute S**: Measure the average pairwise similarity (cosine, correlation) between adjacent probability vectors, or the entropy of the token choices. Higher similarity → higher stability.
4. **Visualize**: Plot each reasoning trace in the (GP, S) plane. Aggregate many traces to see the model’s typical reasoning profile.
5. **Compare**: Contrast different models, prompting strategies, or fine‑tuning regimes by their GP/S distributions.

The output is a rich diagnostic that goes beyond “correct/incorrect” to ask *how* the model arrived there.

---

## 📊 Key Findings and Insights

The TRACED paper applied this to several LLMs (GPT‑4, Claude, LLaMA) on reasoning benchmarks like GSM8K, MATH, and logic puzzles. What they discovered:

- **Scalar accuracy masks reasoning flaws**. Models with similar final accuracy can have dramatically different GP/S profiles. For example, one model might show high GP and high S (confident, steady climb), while another has high GP but low S (confident but wobbly—potentially overfitting shortcuts).
- **Chain‑of‑thought prompting improves GP but can reduce S**. CoT encourages the model to build confidence step‑by‑step, but sometimes introduces instability as the model wanders off‑track before recovering.
- **Model scale correlates with stability**. Larger models tend to have higher S, suggesting they reason more coherently.
- **Fine‑tuning on reasoning data boosts GP**. Optimizing for correct answers increases the upward trend of confidence, but may sometimes sacrifice stability if the model learns to “jump” to conclusions.
- **Adversarial examples target stability**. Carefully crafted inputs can cause a model’s confidence trajectory to oscillate wildly while still landing on the right answer—a hidden vulnerability scalar metrics miss.

---

## 💡 Why This Matters for Developers and Researchers

### Better Model Selection
When choosing a model for a reasoning‑heavy application, don’t just look at accuracy. Check its GP/S profile. A model with high GP and high S is more reliable and trustworthy than one with high GP but low S, even if both get the same final score.

### Prompt Engineering Insights
TRACED can guide prompt design. Does adding “Let’s think step by step” improve GP? Does few‑shot with coherent examples stabilize S? These questions become measurable.

### Training Objectives
Incorporate GP or S directly into the loss function to train models that reason more geometrically sound. A model that learns to maintain stable confidence growth may generalize better.

### Safety and Monitoring
Deployed reasoning systems could have their reasoning traces monitored in real‑time. A sudden drop in S might indicate prompt injection or distribution shift, triggering a fallback or human review.

---

## 🚀 Beyond LLMs: Generalizing the Idea

The TRACED principle—evaluating process geometry—could apply to any sequential decision‑making system:

- **Robotic planning**: How does confidence in action selection evolve? Is the plan converging or oscillating?
- **Algorithmic problem solving**: Measure progress of a proof search or optimization algorithm.
- **Human‑AI collaboration**: Track whether the AI’s reasoning is becoming more or less stable as it interacts with a user.

Essentially, TRACED turns “reasoning” into a geometric object we can measure, compare, and optimize.

---

## Conclusion

Scalars are easy to compute and compare, but they flatten the rich topography of reasoning into a single hill. TRACED restores that topography, letting us see the valleys, peaks, and plateaus of an LLM’s thought process. As AI systems become more autonomous and safety‑critical, we need evaluation that captures *how* they think, not just *what* they conclude. Geometric progress and stability offer a compelling multidimensional alternative. The next time someone quotes a single accuracy number for a reasoning model, ask: “But what’s its TRACED fingerprint?” The answer might reveal more than the number ever could.

*Paper: arXiv:2603.10384v1*