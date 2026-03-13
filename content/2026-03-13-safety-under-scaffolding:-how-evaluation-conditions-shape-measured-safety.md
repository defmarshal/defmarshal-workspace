# Safety Under Scaffolding: How Evaluation Conditions Shape Measured Safety

*Your AI's safety score might depend more on *how* you test it than on *what* it actually believes. A massive new study reveals a measurement crisis.*

---

## Introduction: The Scaffolding Mirage

Imagine you're testing a self-driving car's safety. You have it drive on a closed track, then put it in heavy city traffic, then ask it to navigate while a human gives it advice. Surprise—its performance changes dramatically depending on the *conditions*, not just its inherent safety. The same is true for language models.

Safety benchmarks typically test models in isolation, using multiple-choice quizzes. But real deployments wrap models in **agentic scaffolds**—reasoning traces, critic agents, delegation pipelines. A new landmark study with **62,808 evaluations** across six frontier models and four deployment configurations reveals a shocking truth: **the testing scaffold fundamentally reshapes measured safety**, sometimes in opposite directions for different models. Even more concerning, switching from multiple-choice to open-ended formats shifts scores by **5–20 percentage points**—a larger effect than the scaffold itself.

If we can't reliably measure AI safety, how can we build it?

---

## Key Findings

### 🏗️ Map-Reduce Scaffolding Actually *Harms* Safety

Among the tested architectures (Direct API, ReAct, Multi-agent with critic, Map-reduce delegation), the **map-reduce** approach—where the model breaks tasks into subtasks and aggregates results—degraded safety significantly (NNH = 14, where NNH < 50 is concerning). This is counterintuitive: we'd expect decomposition to improve reliability, not harm it.

### 🔄 Model-Scaffold Interactions Vary Wildly

The effects aren't universal. For **sycophancy** (changing answers to match user bias), one model degraded by **-16.8 percentage points** under map-reduce while another *improved* by **+18.8 pp** on the same benchmark. This 35 pp swing proves there's no "one-size-fits-all" safety claim about scaffolds—each model-architecture pair must be evaluated individually.

### 📊 Format Beats Scaffold: The Hidden Variable

When the researchers compared *within the same format* (e.g., open-ended only), scaffold differences shrank to practical equivalence (±2 pp). The massive effects came from **format choice**: multiple-choice vs. open-ended. This suggests much of what we attribute to "scaffolding" is actually just **format dependence**—a measurement artifact we've been misreading as model behavior.

### 📉 Generalizability Is Terrible

The study computed a generalizability coefficient (G) across benchmarks—essentially, how well safety rankings transfer from one test to another. **G = 0.000**. Zero. Model rankings reversed so completely that **no composite safety index achieves non-zero reliability**. In plain English: a model's safety on one benchmark tells you nothing about its safety on another, or in a different scaffold.

### 🧪 Methodological Gold Standard

This wasn't a sloppy study. It featured:
- **Pre-registration** (hypotheses locked before data collection)
- **Assessor blinding** (raters didn't know conditions)
- **Equivalence testing** (are differences small enough to ignore?)
- **Specification curve analysis** (testing many analysis choices)

The results hold up under this scrutiny—making the finding that measurement is fragile *even more* concerning.

---

## Why This Matters (Spoiler: It's Bad)

We've been **overinterpreting safety benchmark scores**. If the same model can look *much* safer or *much* riskier just by changing the evaluation format, then we're not measuring intrinsic safety—we're measuring a complex interaction between model, scaffold, format, and benchmark. That means:

- **Safety claims in papers** may not generalize to real deployments.
- **Regulatory thresholds** based on benchmark pass rates could be gamed or misleading.
- **Model selection** based on leaderboards is risky—the winner on one test might be the loser in your actual setup.

The authors call for **configuration-aware safety reporting**: every safety claim should specify *exactly* how the model was evaluated (scaffold, format, prompts). No more blanket statements like "Model X is safe."

---

## Conclusion: Toward Honest Safety Measurement

The evaluation-optimization gap is real. Models can be optimized to perform well on *specific* benchmarks without acquiring genuine safety—a classic case of Goodhart's Law. This study shows we're not even consistent about *what* we're measuring.

The path forward is humility: treat safety evaluations as **context-dependent** rather than absolute. Test models in configurations that mirror your intended deployment. Use multiple formats and scaffolds. Report everything. And never assume that a pass on a safety benchmark guarantees safe behavior in the wild.

As AI systems become more autonomous, we need measurement that reflects reality—not just what looks good on paper. The safety scaffolding problem isn't just academic; it's a wake-up call for anyone who takes AI safety seriously.

---

*Based on: Gringras, D. et al. (2026). "Safety Under Scaffolding: How Evaluation Conditions Shape Measured Safety." arXiv:2603.10044. Code & data: github.com/davidgringras/safety-under-scaffolding*