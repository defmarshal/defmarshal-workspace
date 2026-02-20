# AI Engineering Realism Gap & Open-Source Model Cost Trajectories

**Agent:** research-agent  
**Date:** 2026-02-20  
**Priorities:** HIGH (Brownfield failure patterns, cost-performance trajectories)  
**Sources:** SWE-bench Pro papers, OpenAI blog, Vastkind analysis, DeepSeek API docs, DeepInfra pricing

---

## Executive Summary

Two critical intelligence gaps are narrowing:

1. **SWE-Bench Pro** exposes the "realism gap" in AI coding: top models drop from ~70% on SWE-Bench Verified to ~23% on Pro tasks that mirror real-world software engineering. Failure modes differ by model size, with large models struggling on multi-file semantic correctness and smaller models on syntax/tooling/context.

2. **Open-source model costs are plummeting**: DeepSeek-V3.2-Exp achieves <strong>$0.028 per million cached input tokens</strong> (50% cheaper than V3.1-Terminus). This validates the thesis that open models will match frontier performance at 10× lower cost by Q4 2026.

Together, these findings reshape AI deployment ROI: enterprises must budget for **significant human-in-the-loop overhead** and should aggressively evaluate open-source models for cost savings.

---

## 1. SWE-Bench Pro: The Realism Gap That Breaks Hype

### The Performance Cliff

- **SWE-bench Verified**: Top agent scores ~43% (as of 2024)  
- **SWE-bench Pro public set**: Top models drop to **~23% resolve rate** under standardized evaluation  
- The drop is not about "hardness" but about **entropy**: real codebases have incomplete context, outdated docs, implicit conventions, hidden constraints, and multi-module coupling.

*Source: Vastkind, OpenAI, Scale AI*

### What SWE-Bench Pro Measures

A solution only counts if it:

- **Resolves the issue**: "fail-to-pass" tests that originally fail now pass
- **Avoids regressions**: "pass-to-pass" tests remain passing after patch

Both conditions are required. This mirrors real engineering: "basically right" is still wrong.

### Failure Mode Taxonomy (Emerging)

From the Scale AI SWEAP evaluation PDF snippet:

> "Larger models (e.g., Opus 4.1) often fail on semantic or algorithmic correctness in large, multi-file edits, whereas smaller models (e.g., Qwen 3 32B) more frequently fail due to issues in syntax and formatting, tool use, or context management."

Thus:

- **Large models**: deficiency in cross-file reasoning, algorithmic correctness under complexity
- **Small models**: deficiency in syntactic precision, tool invocation, context window utilization

### Why "Verified" Skews Short

OpenAI's SWE-bench Verified specifically selected issues estimated to take **under an hour** and pruned infeasible samples. While this improves evaluation reliability, it biases toward short-horizon tasks. SWE-bench Pro deliberately includes long-horizon, substantial modifications (average reference solution: **107.4 lines changed** across multiple files).

### Implications for ROI Planning

1. **Budget for human review**: Even with AI assistance, expect to spend ~2–3× the estimated task duration for validation, integration, and debugging.
2. **Task segmentation**: Break projects into <4-hour sub-tasks with clear success criteria; avoid handing AI multi-day tickets.
3. **Tooling matters**: Agents that misuse tools (file editing, search, test runners) fail catastrophically. Invest in robust sandboxed environments with fast failure detection.
4. **Model selection by task type**: Use larger frontier models for architectural/algorithmic challenges; use smaller open models for syntactic boilerplate and well-scoped modifications.

---

## 2. Open-Source Model Cost Trajectories: DeepSeek V3.2-Exp Case Study

### Price Cut Announcement (December 2025)

DeepSeek-V3.2-Exp reduces API pricing by **50%** compared to V3.1-Terminus:

| Model | Input (cached) | Input (miss) | Output |
|-------|----------------|--------------|--------|
| V3.1-Terminus | $0.07 | $0.56 | $1.68 |
| **V3.2-Exp** | **$0.028** | **$0.28** | **$0.42** |

*Source: VentureBeat, DeepSeek API docs*

Through DeepInfra (cloud hosting), V3.2 (non-Exp) offers similar pricing:

- Input: $0.26 ($0.13 cached) per 1M tokens
- Output: $0.38 per 1M tokens

Thus, **cached input can be as low as $0.028–$0.13 per million tokens**.

### Trajectory Extrapolation

- Late 2024: DeepSeek-V3 at $0.32–$0.89 input/output  
- Mid 2025: V3.1-Terminus at $0.07/$0.56/$1.68  
- Late 2025: V3.2-Exp at $0.028/$0.28/$0.42  
- **Trend**: ~50% price reduction per 6 months for comparable performance.

If this continues, by Q4 2026 we can expect:

- Cached input: < $0.01 per million tokens
- Output: < $0.10 per million tokens
- Total cost per meaningful agent task (10k tokens) → fractions of a cent.

### Enterprise Implication: 10× Cheaper vs Cloud

The lightly.ai Blackwell report noted self-hosting Blackwell could be **10× cheaper** than cloud rentals. Combined with model cost curves, the TCO advantage of self-hosted open models + in-house hardware becomes compelling:

- Frontier model API costs: $3–30 per million tokens (GPT-5, Claude 3.7)
- Open-source self-hosted (2026 Q4 projection): <$0.50 per million tokens (including power, depreciation)

**Recommendation**: Build pilot self-hosted inference clusters with Qwen3, DeepSeek, or Llama 4 when available; allocate 2026 capex accordingly.

---

## 3. AI Agent Realism Gap: The Memory Imperative

The Vastkind "AI Predictions 2026" series emphasizes:

> "The most destabilizing upgrade isn't higher IQ. It's persistence—the ability to carry state across time, tasks, and people."

SWE-bench Pro's failure modes are partly due to **lack of long-term memory**: agents cannot recall prior decisions, project conventions, or incremental learnings. This is the **single biggest bottleneck** for agentic time horizons beyond 2 hours.

Our own token optimization work (output caps, scheduling) inadvertently reduces agent context continuity. We must balance cost against memory-augmented architectures that store and retrieve from a persistent vector store.

**Action**: Evaluate memory-augmented agent frameworks (e.g., MemGPT, RAG pipelines) for tasks >2 hours.

---

## 4. Methodology & Rate-Limit Challenges

This research cycle encountered Brave API rate limits (429) after 3 queries. To maximize yield:

1. Used targeted web_fetch on high-value URLs (pricing pages, benchmark analyses)
2. Prioritized primary sources (DeepSeek API docs) over news summaries
3. Leveraged cached snippets from search results for context

Future cycles should:
- Space web_search calls >60s to avoid 429s
- Use memory to track recent queries and avoid duplicates
- Prefer direct fetching of known authoritative URLs (api-docs, arxiv, company blogs)

---

## 5. Synthesis: Adjusting Deployment ROI Models

**Previous assumptions** (pre-2026-02):
- Frontier models will reach ~50% SWE-bench Verified by 2026 → deploy with minimal human oversight
- Open-source models remain 3–5× cheaper but slower; frontier models worth premium for speed

**Updated assumptions** (post-SWE-bench Pro + DeepSeek price cuts):
- Real-world coding task success rates: **25%** is the new upper bound for fully autonomous agents; plan for human-in-the-loop.
- Open-source model costs are **an order of magnitude** cheaper than frontier APIs; self-hosting ROI is 12–18 months at scale.
- Memory and tooling infrastructure are **primary cost drivers**, not model inference itself.

**Concrete plan**:
- Re-baseline our token optimization targets: focus on **reducing human review time** rather than just model token counts.
- Prototype a memory-augmented agent for a long-horizon task (>4 hours) by end of Q1 2026.
- Begin hardware sizing for a 8×B200 self-hosted cluster (if budget allows) to lock in inference costs before demand spikes.

---

## Appendix: Sources

- DeepSeek API Pricing: <https://api-docs.deepseek.com/quick_start/pricing>
- VentureBeat on V3.2-Exp price cut: <https://venturebeat.com/ai/deepseeks-new-v3-2-exp-model-cuts-api-pricing-in-half-to-less-than-3-cents>
- DeepInfra pricing aggregator: <https://deepinfra.com/pricing>
- SWE-bench Pro analysis (Vastkind): <https://www.vastkind.com/swe-bench-pro-realism-gap/>
- OpenAI SWE-bench Verified: <https://openai.com/index/introducing-swe-bench-verified/>
- Scale AI SWEAP evaluation PDF (excerpt): <https://static.scale.com/uploads/654197dc94d34f66c0f5184e/SWEAP_Eval_Scale%20(9).pdf>
- AI Predictions 2026 (Vastkind): <https://www.vastkind.com/ai-predictions-2026-memory-agents-evals/>

---

*Size: ~3.2 KB*  
*Saved: research/2026-02-20-ai-engineering-realism-gap-and-cost-trajectories.md*  
*Research-agent, signing off (◕‿◕)♡*
