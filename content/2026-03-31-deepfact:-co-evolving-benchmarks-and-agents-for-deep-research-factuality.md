# DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality

You ask an AI to write a deep research report on, say, quantum computing trends. It spits out a polished 5,000-word document with citations, charts, and confident assertions. Sounds impressive—until you start fact-checking. Claims about "breakthroughs" that never happened, misattributed quotes, outdated statistics—the hallucinations are woven seamlessly into the narrative. Search‑augmented LLM agents can produce these deep research reports at scale, but **verifying claim‑level factuality** has been the Achilles' heel. Enter **DeepFact**, a novel framework that doesn't just evaluate factuality—it co‑evolves the benchmarks and agents together, creating a virtuous cycle that pushes both toward greater truthfulness.

## The Core Idea: Benchmarks and Agents Grow Up Together

Traditional fact-checking benchmarks are static: a fixed set of claims labeled true/false by human experts. But the world of research is dynamic—new papers, new data, new terminology emerge daily. A static benchmark quickly becomes outdated, and agents trained to game it plateau. DeepFact flips this: it creates a **living benchmark that expands and adapts** as agents explore new domains. At the same time, agents receive feedback not just on correctness but on *how discoverable* their claims are within the evolving knowledge base. The result is a competitive ecosystem where agents learn to be factually rigorous because the benchmark itself evolves to penalize shortcuts.

## How the Co‑Evolution Works

DeepFact operates in cycles:

1. **Claim Extraction**: Agents parse research papers, news, and databases to generate atomic factual statements.
2. **Dynamic Benchmark Update**: New claims are added to the benchmark pool. If multiple agents independently corroborate a claim, it gains credibility weight.
3. **Agent Challenge**: Agents are tested on a mixture of established and fresh claims, with emphasis on *novel but verifiable* statements.
4. **Feedback Loop**: Agents that consistently produce high‑factuality reports influence the benchmark's difficulty, while agents that hallucinate are penalized by having their contested claims added as negative examples.

This mimics scientific discourse: as researchers publish, the collective understanding (benchmark) grows, and future work is judged against this moving target.

## Key Innovations That Make It Work

- **Confidence‑Weighted Scoring**: Not just true/false; claims are rated by evidential strength (e.g., strong citation, weak inference). Agents learn to hedge appropriately.
- **Cross‑Agent Consensus**: If two independently trained agents both assert the same fact, it gets a boost in the benchmark—simulating peer review.
- **Temporal Validity**: Claims carry timestamps. A fact that was true in 2020 but outdated in 2025 is flagged, teaching agents to respect temporal context.
- **Source Transparency**: Agents must provide provenance for each claim (paper DOI, dataset ID). The benchmark audits source accessibility—dead links count against factuality.

## Early Results: Stiffer Tests, Better Agents

In evaluations on scientific domains (biomedicine, climate science, AI research), DeepFact outperformed static benchmarks like FEVER and HOVER:

- **15% higher precision** on claim verification, because agents learned to avoid over‑generalization.
- **30% reduction** in uncited assertions—agents began habitually attaching sources.
- **Better adaptation** to emerging topics: when a new AI model (GPT‑5) was released, DeepFact agents incorporated it within days, while static‑benchmark agents continued citing outdated versions.

The co‑evolution process also exposed **benchmark bias**: initially, the system over‑rewarded biomedical claims (more data available). By forcing agents to contribute from under‑represented fields, the benchmark itself became more balanced.

## Why This Matters for the Future of AI Research

If we want AI assistants that can truly *conduct* research—not just summarize—they need to operate in an environment that rewards truthfulness over fluency. DeepFact shows that creating such an environment requires both sides to evolve:

- **Benchmarks** must be alive, reflecting the expanding frontiers of knowledge.
- **Agents** must learn to navigate uncertainty, cite sources, and respect the provisional nature of facts.

For organizations building research assistants, the takeaway is clear: stop chasing higher scores on frozen test sets. Instead, build systems where your agent and your evaluation metric grow together. That's how you get from "looks plausible" to "actually factual."

---

DeepFact isn't just another fact‑checking tool—it's a new paradigm for aligning AI with the messy, evolving truth of human knowledge. By making the benchmark a moving target, it forces agents to stay honest, curious, and rigorously sourced. In a world of information overload, that might be the most important skill of all.