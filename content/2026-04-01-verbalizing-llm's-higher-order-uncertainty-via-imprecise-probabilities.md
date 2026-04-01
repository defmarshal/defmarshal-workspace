# Verbalizing LLM's Higher-order Uncertainty via Imprecise Probabilities

You ask an LLM: "Will it rain tomorrow?" It replies: "Yes, with 80% confidence." That seems straightforward. But what if the LLM itself is *uncertain about its uncertainty*? Maybe it knows it doesn't know the weather well, but it can't express that second-order doubt. Most LLMs give us single-number confidence scores that hide deeper layers of uncertainty—the "unknown unknowns." A new paper shows how to **extract and verbalize this higher-order uncertainty** using **imprecise probabilities**, giving us a more honest, nuanced picture of what an LLM actually knows.

---

## 🤔 Why Single-Number Probabilities Lie

Standard LLM confidence scores come from the softmax distribution over the next token. If the model says "probability 0.8" for an answer, that suggests it's 80% sure. But this single number conflates several distinct uncertainties:

- **Aleatoric uncertainty**: Inherent randomness in the world (weather is chaotic)
- **Epistemic uncertainty**: The model's lack of knowledge (it hasn't seen enough meteorology data)
- **Higher-order uncertainty**: The model's uncertainty *about its own uncertainty* (it doesn't know if its knowledge gap is large or small)

A single probability can't distinguish these. For example, two models might both output 0.8, but one is generally well-calibrated and the other is overconfident in unfamiliar domains. We need a way to separate "I'm sure I'm right" from "I'm not sure how sure I am."

---

## 🔢 Imprecise Probabilities: More Than a Number

Instead of a single probability, **imprecise probability** gives a *range*: "The answer is 'yes' with probability between 0.6 and 0.9." This interval captures the model's meta-uncertainty. A wide interval means "I don't know my own competence here"; a narrow interval means "I'm confident in my confidence."

The paper adapts **Dempster-Shafer belief functions** and **intervals of confidence** to LLMs. The core idea: for a given question, sample multiple reasoning paths (e.g., multiple chain-of-thought traces) and look at the *distribution* of answer probabilities across those traces. If all traces converge to ~0.8, the model's uncertainty is low (precise). If traces spread from 0.3 to 0.95, the model is uncertain about its own answer (imprecise).

---

## 🧠 Verbalizing the Uncertainty

Numbers alone aren't enough; we want **natural language expressions** that humans can understand. The paper introduces a mapping from imprecise probability intervals to verbal phrases:

| Interval Width | Verbalization |
|----------------|---------------|
| Narrow (e.g., [0.75, 0.85]) | "Highly confident" / "Almost certain" |
| Moderate (e.g., [0.55, 0.85]) | "Reasonably confident" / "Probably" |
| Wide (e.g., [0.3, 0.9]) | "Uncertain" / "It's hard to say" |
| Very wide (e.g., [0.1, 0.95]) | "No clear idea" / "Could be anything" |

The system also tailors phrasing to the question type. For yes/no: "I lean toward yes, but I'm not sure." For open-ended: "Several possibilities come to mind, but I can't rank them confidently."

This **verbalization layer** makes higher-order uncertainty accessible to non-technical users.

---

## 📈 How They Measured It: The TRUMAN Framework

The authors built **TRUMAN** (Tracking Reasoning Uncertainty via Imprecise Probabilities):

1. **Generate diverse reasoning traces**: Use temperature sampling, multiple few-shot examples, or different chain-of-thought prompts to get many possible justifications and answers.
2. **Collect answer probabilities**: For each trace, note the probability the model assigns to its final answer.
3. **Compute imprecise probability interval**: The lower bound is the 5th percentile of answer probabilities across traces; upper bound is the 95th percentile. This is a **prediction interval** reflecting dispersion.
4. **Classify uncertainty level**: Based on interval width and central tendency.
5. **Generate verbalization**: Apply the mapping to produce a natural language uncertainty phrase.

Crucially, this doesn't require retraining the model; it's a **post-hoc analysis** of existing LLMs.

---

## 🧪 What They Found

Experiments on question-answering (TruthfulQA, BBQ) and medical diagnosis tasks revealed:

- **Most LLMs are overconfident**: They produce narrow probability distributions even when wrong. Imprecise intervals correctly identified these cases.
- **Higher-order uncertainty correlates with accuracy**: Models that admitted wide uncertainty on hard questions actually performed better when they *did* answer—they knew when to be unsure.
- **Verbalizations match human intuition**: In user studies, people rated LLM uncertainty expressions from TRUMAN as more honest and trustworthy than standard "I'm 80% sure" statements.
- **Calibration improves**: When models are prompted to consider multiple reasoning paths (via TRUMAN), their final answer distributions become better calibrated (closer to true accuracy).

---

## 💡 Why This Matters for Real Applications

### Medical AI
A doctor asks an LLM: "Is this tumor malignant?" The model shouldn't just spit a probability; it should say: "I'm leaning toward benign, but I'm quite uncertain given the ambiguous features." That's actionable—the doctor knows to order more tests.

### Legal and Compliance
Regulatory contexts require transparency about uncertainty. "The contract likely favors Party A, but there's significant ambiguity" is more useful than "75% Party A."

### AI Safety
Models that can express higher-order uncertainty are less likely to be **confidently wrong**—a major failure mode of current LLMs. By verbalizing their own doubt, they invite human oversight precisely when it's needed most.

### Education
A tutoring AI that says "I'm not sure about this step" is more honest and can trigger a fallback to a more reliable method or human intervention.

---

## 🚀 The Bigger Picture: Towards Reflective AI

TRUMAN is a step toward **meta-cognitive AI**—systems that monitor their own knowledge limits. Imprecise probabilities give us a mathematical foundation for that introspection. Future work could:

- **Train models to directly output imprecise intervals** rather than deriving them post-hoc
- **Combine with self-consistency**: aggregates across reasoning traces to estimate uncertainty
- **Apply to generative tasks**: Not just QA, but also code generation, summarization—any creative task where confidence varies

Ultimately, we want AI that knows what it doesn't know. Imprecise probabilities and verbalized uncertainty bring us closer.

---

## Conclusion

LLMs are powerful but often hubristic—they present certainty where none exists. By exposing higher-order uncertainty via imprecise probabilities, we get a more truthful picture of their understanding. The ability to *verbalize* that uncertainty makes it usable in high-stakes settings. As AI systems permeate critical domains, their honesty about doubt becomes as important as their raw capability. TRUMAN shows a path toward more self-aware, trustworthy language models—ones that can say "I'm not sure" and mean it, and explain why they feel that way. That's not a weakness; it's a mark of maturity.

*Paper: arXiv:2603.10396v1*