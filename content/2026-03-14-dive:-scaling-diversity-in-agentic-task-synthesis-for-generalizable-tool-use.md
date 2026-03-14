# DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use

*Why your AI agent still fails at new tools (and how a simple inversion trick fixes it)*

---

## Introduction: The Generalization Gap

Imagine training an AI to use a set of 10 tools—web search, calculator, calendar, email. It aces tests involving exactly those tools. Then you give it a new tool, say a map API, and ask it to plan a route. Suddenly it stumbles, even though the new tool is conceptually similar. This **generalization gap** plagues current tool-using LLMs: they're brittle when faced with unfamiliar tool combinations or task families.

Recent work synthesizes agentic tasks for post-training (think: "search for X, then email Y"), but scaling diversity while keeping tasks *executable* and *verifiable* has been a fundamental tension. Most approaches either churn out narrow, repetitive data (deep-research style) or generate wild, unsolvable queries.

Enter **DIVE**—a brilliantly simple inversion: instead of dreaming up tasks first and hoping tools can handle them, DIVE **executes diverse real-world tools first** and reverse-engineers tasks from the resulting traces. This "evidence-first" recipe yields tasks that are guaranteed executable (they already happened) and verifiable (outputs are real). The result? Generalization gains that blow past quantity scaling—even with 4× less data.

---

## Key Insights

### 🎯 The Core Problem: Insufficient Diversity

Current agentic training data suffers from **structural monotony**:
- Fixed toolsets (e.g., only web search + browse)
- Narrow task families (deep-research loops)
- Template-like variations (changing entities but not patterns)

This leads to **rigid routines** (search→browse loops) that fail on out-of-distribution (OOD) tasks like clinical diagnosis with medical lookup tools.

### 🔄 Invert the Pipeline: Tools First, Tasks Later

DIVE’s central innovation: **execute before you synthesize**.
- Instead of "query → check if tools can solve it"
- DIVE does: "pick a diverse toolset → run real tools → derive tasks from the evidence traces"

This gives **grounding by construction**: every task is provably solvable because it’s derived from an actual execution. No more unverifiable hypotheticals.

### 📈 Two Levers for Diversity

DIVE scales structural diversity along two controllable axes:

1. **Tool-pool coverage** – Include a broad spectrum of tools (general-purpose + domain-specific)
2. **Per-task toolset variety** – Randomly sample different combinations of tools for each task

They built a pool of **373 validated tools** across five domains (general + 4 expert). This variability forces the model to learn flexible tool-use patterns rather than rote sequences.

### 🔁 The Evidence Collection–Task Derivation Loop

Each synthesis cycle runs a two-stage loop:

1. **Evidence Collection**: Interleave multi-step reasoning with real tool use to gather logically related evidence. This dynamically induces diverse tool-use patterns (retrieval-only, retrieval→analyze, etc.).
2. **Task Derivation**: Observe the accumulated evidence and reverse-derive query–answer pairs strictly entailed by the traces. As evidence grows, tasks are refined to stay grounded while increasing diversity.

The loop continues until a coherent, verifiable task is constructed. It’s like watching a skilled assistant work, then turning their actions into teachable moments.

### 📊 Results: Diversity > Quantity

Training **Qwen3-8B** on DIVE data (48k SFT + 3.2k RL) yielded spectacular gains:

- **+22 average points** across 9 OOD benchmarks
- **+68% improvement** over the strongest 8B baseline
- Most strikingly: **Diversity scaling consistently outperformed quantity scaling**, even when DIVE used **4× less data**.

Translation: How *varied* your training tasks are matters more than how *many* you have. This is a paradigm shift for data-centric AI.

---

## Why This Matters for Real-World Agents

DIVE isn’t just an academic exercise—it directly addresses the **deployment gap** that plagues real-world AI assistants:

- **Tool churn**: New APIs appear all the time. An agent trained on diverse tool patterns adapts faster.
- **Domain shifts**: Moving from web search to medical lookup or financial analysis becomes less painful.
- **Implementability**: DIVE uses real-world tools, not simulations, so the learned behaviors transfer directly.
- **Efficiency**: Less data needed means cheaper training and faster iteration.

For organizations building agentic systems, DIVE suggests a new best practice: prioritize *diversity of tool experiences* over sheer volume of examples. Collect traces from many tools, then derive tasks from those traces. Your agent will generalize like a champ.

---

## Conclusion: Diversity as the New Scaling Law

The AI field has long operated on a "bigger is better" mentality: more data, more parameters, more compute. DIVE flips the script for agentic training: **diversity beats quantity**. By inverting the synthesis pipeline and grounding tasks in real tool executions, DIVE produces training data that is both high-quality and structurally varied.

The result is tool-using LLMs that don’t just memorize routines—they learn to *adapt* to new tools and tasks. As AI agents proliferate across industries, that kind of generalization isn’t just nice to have; it’s essential for robustness and safety.

The lesson? When teaching AI to use tools, don’t just give it more examples. Give it *different* examples. Build a diverse toolbox, let the AI explore, and then turn those explorations into lessons. That’s the DIVE way—and it might just be the blueprint for the next generation of generalist agents.

---

*Based on: Chen, A. et al. (2026). "DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use." arXiv:2603.11076v1. Accepted at ICML 2026 (Machine Learning track).*