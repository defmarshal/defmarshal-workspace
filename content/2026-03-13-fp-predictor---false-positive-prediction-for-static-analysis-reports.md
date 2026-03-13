# FP-Predictor — False Positive Prediction for Static Analysis Reports

*What if your security scanner could tell you which warnings are *real*? A new AI model cuts through the noise with 96%+ accuracy.*

---

## Introduction: The SAST Alarm Fatigue Problem

Static Application Security Testing (SAST) tools are like hypersensitive smoke detectors — they catch real fires (vulnerabilities), but they also go off every time you make toast. For developers, this **false positive flood** is exhausting: hours wasted investigating phantom issues, real threats get buried, and trust in automated security erodes.

Enter **FP-Predictor**, a groundbreaking Graph Convolutional Network (GCN) that learns to separate true security warnings from false alarms. By analyzing the *structure* of code with Code Property Graphs (CPGs), it achieves near-perfect accuracy on benchmark datasets. This isn't just another ML paper — it's a tool that could save developers thousands of hours and make SAST tools actually trustworthy.

---

## Key Points

### 🧠 How It Works: GCNs Meet Code Graphs

FP-Predictor represents vulnerable code snippets as **Code Property Graphs** — a rich fusion of abstract syntax trees, control flow graphs, and program dependence graphs. Think of it as a semantic blueprint of the code, capturing both syntax and meaning. A Graph Convolutional Network then learns patterns that distinguish true positives from false ones. The model trains in just **~5 minutes** on a consumer‑grade GPU (RTX 4090), making it surprisingly practical.

### 📈 Results: 100% Accuracy on Test, 96.6% in the Wild

On the **CamBenchCAP** dataset (cryptographic API misuse), FP-Predictor hit **100% accuracy** with an 80/20 train‑test split. That's almost too good to be true — but it held up when tested on a completely different benchmark (**CryptoAPI-Bench**), reaching **96.6% accuracy**. This suggests the model learned *generalizable* signals of false positives, not just dataset quirks.

### 🔍 The Security‑Aware Mindset

What's fascinating is why the model works: when researchers inspected "misclassifications," many turned out to be **actual security weaknesses** that the ground truth had missed. In other words, FP-Predictor is *conservative* — it prefers to flag something as a true positive rather than risk dismissing a real vulnerability. That's the right instinct for security: better safe than sorry.

### ⚠️ Current Limitations

- **Interprocedural gaps**: The CPG doesn't fully connect call graphs across functions, missing some control‑flow context.
- **Tool specificity**: Trained on CogniCrypt SAST output; may not generalize to other SAST tools without retraining.
- **Interpretability**: GCN decisions are still a black box; explainability techniques are needed for developer trust.

---

## Why This Matters

False positives aren't just annoying — they're costly. Security teams spend **up to 50% of their time** on triage. If FP-Predictor can filter out 90%+ of false alarms automatically, that's a massive productivity boost. More importantly, it restores trust in SAST tools. When developers believe the scanner is *right* most of the time, they'll actually fix the issues it raises.

The approach also opens the door to **tool-agnostic triage**: you could train a universal model that understands multiple SAST outputs and gives you a single, confidence‑scored list of real vulnerabilities.

---

## Conclusion: From Noise to Signal

FP-Predictor proves that not all SAST noise is inevitable. With the right representation (CPGs) and model (GCNs), we can learn to distinguish real security flaws from spurious warnings. The next step is integration: plug this into CI/CD pipelines, extend it to other vulnerability classes, and make it explainable. The dream? A security scanner that's *quiet* because it only reports what matters. FP-Predictor brings us one step closer.

---

*Based on: Ohlmer, T. et al. (2026). "FP-Predictor – False Positive Prediction for Static Analysis Reports." arXiv:2603.10558. Accepted at STATIC '26 (ICSE 2026 workshop).*