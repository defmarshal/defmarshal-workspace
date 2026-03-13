# The System Hallucination Scale (SHS): A Minimal yet Effective Human-Centered Instrument for Evaluating Hallucination-Related Behavior in Large Language Models

*Introducing a simple, powerful tool to measure how often AI makes things up—from the user's perspective.*

---

## Introduction: Measuring the Unmeasurable?

Hallucinations—where large language models generate fluent, persuasive text that's factually wrong or entirely made up—are one of AI's biggest trust hurdles. But how do we *measure* this phenomenon consistently? Existing benchmarks focus on accuracy and efficiency, missing the nuanced ways hallucinations manifest in real-world interactions.

Enter the **System Hallucination Scale (SHS)**, a lightweight 10-item questionnaire inspired by proven psychometric tools like the System Usability Scale (SUS). Think of it as a "user satisfaction survey" for AI truthfulness. Instead of complex automatic detectors, SHS asks humans to rate their experience: Did the response feel reliable? Were claims supported? Did the model acknowledge uncertainty? With just a 5-point Likert scale, SHS delivers rapid, interpretable insights into factual unreliability, coherence, misleading presentation, and responsiveness to user guidance.

A study with 210 participants validated the scale: high internal consistency (Cronbach's α = 0.87) and strong correlations between dimensions. It's not a benchmark—it's a human-centered lens on how hallucinations *feel* when you're actually using the system.

---

## Key Features

### ✅ Human-Centered, Not Automatic
SHS captures the *user experience* of hallucinations. Participants read model outputs and rate statements like "The information provided was factually correct" or "I felt the system was making things up." This subjective but structured approach reveals how hallucinations manifest in realistic interactions—something automatic metrics miss.

### 📊 Quick, Interpretable, and Domain-Agnostic
At just 10 questions on a 5-point scale, SHS can be deployed in minutes. It works across domains—medical QA, customer support, educational content—without needing specialized adapters. The scoring is straightforward, making results immediately actionable for developers and researchers.

### 🔬 Strong Psychometric Properties
The scale demonstrated excellent reliability (α = 0.87) and significant inter-dimension correlations (p < 0.001). Factor analysis confirmed that SHS measures distinct yet related aspects of hallucination behavior, from factual accuracy to coherence to transparency about uncertainty.

### 🔄 Complementary to Existing Tools
When compared with SUS (usability) and SCS (causability/explainability), SHS filled a unique niche. The three scales together provide a holistic view of an LLM system: Is it usable? Is it explainable? And crucially—can you trust what it says?

---

## Why This Matters

For AI practitioners, SHS offers a practical way to **track hallucination trends** during model iteration, compare different systems, and monitor deployment health. It's especially valuable for high-stakes domains where undetected hallucinations can cause real harm.

The scale also democratizes evaluation—you don't need a team of experts or custom benchmarks. With proper instructions, even non-technical users can contribute meaningful assessments.

---

## Conclusion: A Step Toward Trustworthy AI

Hallucinations won't disappear overnight. But with tools like SHS, we can measure them more systematically, understand their impact on users, and drive improvements that matter. As LLMs become everyday assistants, we need evaluation methods that capture real-world trust—not just lab accuracy. The System Hallucination Scale is a welcome addition to the human-centered AI toolkit.

---

*Based on: Müller, H. et al. (2026). "The System Hallucination Scale (SHS): A Minimal yet Effective Human-Centered Instrument for Evaluating Hallucination-Related Behavior in Large Language Models." arXiv:2603.09989.*