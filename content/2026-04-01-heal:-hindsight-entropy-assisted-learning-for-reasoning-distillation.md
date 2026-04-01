# HEAL: Hindsight Entropy-Assisted Learning for Reasoning Distillation

Large Reasoning Models (LRMs) like GPT-4 can produce impressive chain-of-thought reasoning, but they’re huge and expensive. Smaller models are cheaper, yet they struggle to match that reasoning prowess. Distillation—training a small model to mimic a large one—seems like the obvious solution. But there’s a catch: **reasoning quality varies wildly** across generated traces. Traditional distillation relies on *rejection sampling*: generate many reasoning chains, keep the ones that reach the correct answer, and train on those. This is exhaustive, costly, and still leaves many high-variance traces. What if we could guide distillation more intelligently? Enter **HEAL (Hindsight Entropy-Assisted Learning)**, a clever twist that uses the *future* to teach the past.

---

## 🔍 The Bottleneck: Rejection Sampling Is Wasteful

Rejection sampling works like this:
1. For each training question, have the large model generate dozens of reasoning chains.
2. Check which chains arrive at the correct final answer.
3. Only keep the successful chains to train the small model.

This approach has two big problems:

- **Inefficiency**: Most generated chains may be incorrect, especially on harder reasoning tasks. You waste compute generating traces you’ll discard.
- **Quality blind spot**: Even among *correct* chains, some steps may be shaky or high-entropy (the model was unsure). Training on those can pass shaky reasoning to the small model.

We need a way to **select not just correct chains but *high-confidence* chains**, and to do so without generating thousands of candidates.

---

## 💡 HEAL’s Key Idea: Let Hindsight Guide You

HEAL stands for **Hindsight Entropy-Assisted Learning**. The insight is simple: when we know the correct answer (which we do during training), we can look back at each reasoning step and ask: *How surprised was the model by what it said given the final answer?*

More concretely:

1. Generate multiple reasoning chains for a question (as usual).
2. For each step in each chain, compute the **entropy** of the model’s token distribution *conditioned on the rest of the chain and the final correct answer*.  
   (If the model was highly confident about a step that turned out to be part of a correct solution, that step’s entropy is low. If it was hedging or uncertain, entropy is high.)
3. Aggregate step entropies to get a **chain quality score** (e.g., average entropy).
4. Use this score to **weight** chains during distillation: low-entropy (more certain) chains get higher weight; high-entropy chains get downweighted or filtered.

This is “hindsight” because we use the *known correct answer* to evaluate reasoning steps retroactively. It’s “entropy-assisted” because entropy quantifies the model’s confidence at each step.

---

## 🧠 Why Entropy Works as a Proxy for Reasoning Quality

Why not just use whether the chain is correct? That’s binary and ignores quality within correct chains. A correct chain where the model was confident throughout is more trustworthy than one where it wavered and guessed. Entropy captures that nuance.

HEAL’s weighting ensures the small model learns from **clear, decisive reasoning** rather than from hesitant, rambling traces. This yields:

- **Better generalization**: The small model picks up robust reasoning patterns.
- **Faster convergence**: Fewer high-quality chains suffice, reducing required samples.
- **Improved robustness**: Less chance of learning spurious correlations from noisy chains.

---

## 📈 Results: Better Reasoning with Fewer Samples

The authors evaluate HEAL on mathematical and commonsense reasoning benchmarks (GSM8K, MATH-like datasets). They distill from a large LRM (e.g., GPT-4 or PaLM-2-Large) into a smaller model (e.g., 7B parameters).

Key findings:

- With the same number of generated chains, **HEAL improves accuracy** of the distilled model by 3–5% absolute over rejection sampling alone.
- **Sample efficiency**: HEAL needs only ~30% as many generated chains to reach the same performance as rejection sampling. That’s a huge compute saving.
- **Qualitative improvement**: Human evaluation shows HEAL-distilled models produce more coherent, logically consistent reasoning steps.
- **Entropy thresholding** works best: keeping chains with average step entropy below a learned threshold yields the strongest results.

---

## 🛠️ Practical Implications

HEAL is practical because:

- It adds minimal overhead: entropy computation is cheap compared to chain generation.
- It’s compatible with any LRM that can produce probability distributions (most do).
- It can be combined with other distillation techniques (e.g., outcome supervision, process reward models) for further gains.

For organizations wanting to deploy reasoning models on-device or at low latency, HEAL makes distillation **feasible and cost-effective**.

---

## 🚀 Beyond Reasoning: The Bigger Picture

HEAL’s principle—**use hindsight to assess and weight training data**—could apply to other sequence-generation tasks where quality varies:

- **Code generation**: Weight code snippets by confidence given passing test cases.
- **Dialog generation**: Prefer utterances that are both relevant and fluent given conversation outcome.
- **Planning**: Prefer action sequences that lead to successful episode termination.

Any domain where you have a final outcome (success/failure) can benefit from hindsight entropy weighting.

---

## Conclusion

Distilling reasoning from large to small models is a crucial challenge for practical AI. HEAL introduces a simple yet powerful idea: use the known correct answer to compute stepwise entropy and prioritize high-confidence reasoning traces. This yields more capable small reasoners with fewer samples, making efficient reasoning accessible without relying on massive APIs. As AI systems grow, techniques that make them smaller, faster, and greener—like HEAL—will be essential for widespread impact. Sometimes, looking back is the best way to move forward.

*Paper: arXiv:2603.10359v1*