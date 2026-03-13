# Quantifying Hallucinations in Language Models on Medical Textbooks

*How often do AI doctors make things up? A new study reveals a shocking truth about medical QA.*

---

## Introduction: The Trust Problem

Imagine you're a doctor using a large language model to help diagnose a complex case. The AI responds with confidence, citing detailed medical terminology and sounding extremely plausible. But what if it's **making it up**? Hallucinations—where LLMs generate factually incorrect or unsupported claims—are a serious safety issue in medical AI. Surprisingly, we haven't had a good way to measure just how often this happens when models are tested against *ground-truth medical textbooks*.

A new study from the NIH and University of Maryland tackles this head-on with a clever pipeline called **NameAnonymized**. They extracted passages from public-domain medical textbooks, generated QA pairs, and had medically trained annotators verify every answer. Then they put eight language models through the wringer, including LLaMA-70B-Instruct, to see how many hallucinations would slip through.

The results? Eye-opening. Even when a model's answer *sounds* completely plausible, there's a nearly **1 in 5 chance** it contains unsupported claims. Let's dive in.

---

## Key Findings

### 🏥 The Baseline: LLaMA-70B-Instruct Hallucinates 19.7% of Answers

In the first experiment, the researchers tested LLaMA-70B-Instruct on textbook-grounded medical QA. Shockingly, **19.7% of answers contained hallucinations** (95% CI: 18.6–20.7), even though **98.8% of responses received maximal plausibility scores** from clinicians. This gap between plausibility and factuality is the core danger: AI can sound perfectly reasonable while still being wrong.

### 📊 More Models Tested: Hallucation Rate Correlates with Usefulness

Experiment 2 expanded to eight models of various sizes and training strategies. The key discovery: **lower hallucination rates correlated with higher clinical usefulness scores** (ρ = –0.71, p = 0.058). In other words, models that made up fewer facts were also rated as more helpful by doctors—a strong signal that reducing hallucinations directly improves real-world utility.

### 🧠 Clinicians Agree on What's a Hallucination (Mostly)

The study also measured inter-rater reliability among medical professionals. Results showed **high agreement** for overall usefulness (quadratic weighted κ = 0.92) and **moderate agreement** on identifying hallucinations (τ<sub>b</sub> = 0.06–0.18, κ = 0.57–0.61). This suggests that while clinicians may differ on edge cases, there's a shared sense of what constitutes a factual error in medical text.

---

## Why This Matters (and What's Next)

The NameAnonymized benchmark is a **game-changer** because it's resistant to training data contamination. Every question is linked to an authoritative source paragraph, and any claim not supported by that source is marked as a hallucination. This gives us a clean, reproducible measure of factual reliability—something existing medical QA benchmarks lack.

For practitioners, the message is clear: **Don't trust plausibility alone**. An answer that sounds right may still be wrong. When deploying LLMs in medical settings, you need explicit hallucination detection, retrieval-augmented generation, or human verification loops.

Future work could extend this to other high-stakes domains (law, finance) and test whether retrieval grounding or chain-of-thought prompting reduces hallucinations.

---

## Conclusion: Ground Truth Matters

Medical AI can't afford to make things up. This study proves that even state-of-the-art models hallucinate at concerning rates, and that plausibility is a poor proxy for factuality. The NameAnonymized benchmark offers a path forward—testing models on *unseen* textbook material and penalizing unsupported claims. As we move toward clinical deployment, quantified hallucination rates should be a standard reporting metric, not an afterthought.

The bottom line: **Better benchmarks → Better models → Safer healthcare.** Let's build AI we can actually trust.

---

*Based on: Bartels, D. & Demner-Fushman, D. (2026). "Quantifying Hallucinations in Language Language Models on Medical Textbooks." arXiv:2603.09986.*