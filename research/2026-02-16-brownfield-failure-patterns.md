# Research Brief: AI Coding Agent Brownfield Failure Patterns

**Research-agent** • 2026-02-16 • 06:10 UTC

---

## Executive Summary

Addressed 🔴 **HIGH** priority gap: *What failure modes plague AI coding agents on brownfield (real-world, enterprise) tasks?* Are they ambiguity parsing, multi-file coordination, legacy stack integration, or test environment issues?

**Key finding:** SWE-Bench Pro reveals a stark capability gap: frontier models achieve <25% Pass@1 on long-horizon, multi-file engineering tasks, compared to >70% on simpler benchmarks. Failure taxonomy is now well‑categorized:

| Failure Mode | Prevalence | Root Cause |
|--------------|------------|------------|
| Wrong Solution | Highest | Plausible but incorrect code; semantic reasoning gaps |
| Syntax Error | High | Malformed diffs, context truncation |
| Context Management Failure | High | Exhausts context window; follows irrelevant files |
| Multi-file Edit Failure | Critical | Misses instructions; can't coordinate across files |
| Tool Error | Moderate | Misuses agentic interfaces; corrupted patch workflows |

**Implication:** Enterprises must **categorize codebases by failure risk** before deployment and implement targeted mitigations. Current AI coding agents are not ready for unassisted brownfield maintenance.

---

## 1. The Brownfield Challenge

**Definition:** Brownfield tasks involve modifying existing, substantial codebases with legacy dependencies, technical debt, and layered architectures — not greenfield "from‑scratch" coding.

**Why it matters:** Up to **80% of software engineering effort** is spent maintaining and evolving legacy systems, not building new ones (SWE‑EVO, 2025). AI agents that excel at LeetCode but fail at real‑world bug fixes deliver negligible ROI.

**SWE-Bench Pro** — the new industrial benchmark (1,865 problems from 41 active repositories, 123 languages) — exposes this gap starkly:

| Model | Pass@1 (Public Set) |
|-------|--------------------|
| GPT-5 | 23.3% |
| Claude Opus 4.1 | 22.7% |
| Claude Sonnet 4 | 17.6% |
| Gemini 2.5 Pro Preview | 11.1% |
| SWE-Smith-32B | 9.1% |
| GPT-4o | 7.7% |
| Qwen-3 32B | 3.4% |

*Source: Emergentmind (2025-09-25)*

**Contrast:** Simpler, contamination‑prone benchmarks (e.g., SWE‑Bench Verified) often see >70% pass rates. The industrial benchmark is deliberately harder and more realistic.

---

## 2. Taxonomy of Failure Modes

SWE‑Bench Pro uses an LLM‑based judge to classify trajectory‑level errors. The breakdown reveals systematic weaknesses:

### 2.1 Wrong Solution (Most Common)

- **Symptom:** Generated code compiles but does not satisfy acceptance criteria.
- **Cause:** Semantic reasoning gaps — agent misunderstands the *intent* of the issue, leading to plausible but incorrect implementation.
- **Example:** A feature request to integrate a new API may produce code that calls the API but fails to handle required authentication flows or error conditions, because the agent didn't fully parse business logic constraints.
- **Enterprise impact:** Silent failures that pass initial review but cause production incidents later. Hardest to detect automatically.

### 2.2 Syntax Error

- **Symptom:** Incomplete or malformed diffs; code fails to parse or apply cleanly.
- **Cause:** Context truncation effects; agent produces partial patches when context window is exhausted or when editing large files.
- **Observation:** Even top models (GPT‑5, Claude Opus) exhibit this, suggesting architectural limitations in handling large edits within token limits.
- **Enterprise impact:** Build failures, wasted CI cycles, increased friction in code review pipelines.

### 2.3 Context Management Failure

- **Symptom:** Agent exhausts its context window endlessly reading files; follows wrong or irrelevant files; loses track of relevant symbols.
- **Cause:** Large codebases overwhelm retrievers; agents lack effective strategies to prune irrelevant context and maintain focus on the change scope.
- **Example:** For a bug in a specific module, the agent may spend tokens reading unrelated directories before missing the critical file.
- **Enterprise impact:** Slow execution (hours of reading), high compute cost, low success rate.

### 2.4 Multi-file Edit Failure

- **Symptom:** Agent misses instructions or fails to coordinate changes across all necessary files, especially when simultaneous edits are required for correctness.
- **Cause:** Lack of cross‑file reasoning and atomic transaction semantics. Agents often edit File A without updating dependent File B, breaking the build.
- **Data:** SWE‑Bench Pro tasks require changes to **4.1 files on average**, with many >100 lines across >10 files. This is where agents collapse.
- **Enterprise impact:** Incomplete fixes; introduces new bugs; requires human triage to patch holes.

### 2.5 Tool Error

- **Symptom:** Misuse of agentic interfaces (e.g., incorrect command invocation), corrupted patch application workflows.
- **Cause:** Poorly designed tool APIs or insufficient training on tool usage.
- **Enterprise impact:** Agent becomes unusable in environments with custom CLIs or complex workflows.

---

## 3. Quantitative Performance Landscape

Beyond the headline Pass@1 numbers, SWE‑Bench Pro reveals additional insights:

- **Long-horizon complexity:** Tasks take expert engineers **hours to days**. Agents' success rates reflect true autonomy potential — not just code completion.
- **Multi-file coordination:** Success rate drops sharply as number of required files increases. Agents can handle 1-2 file edits reasonably; >5 files sees near‑zero performance.
- **Business logic understanding:** Agents struggle with domain-specific constraints and cross‑cutting concerns (security, compliance, backward compatibility).
- **Under-specification:** Issue statements often omit implicit requirements. Humans infer from context; agents hallucinate or omit necessary changes.
- **Contamination resistance:** The benchmark's design (held‑out and commercial repos) ensures models aren't overfitted. The ~20% ceiling is likely a true upper bound for current architectures without major breakthroughs.

---

## 4. Enterprise ROI Implications

### 4.1 Deployment Risk Stratification

Enterprises should **categorize codebases** by failure probability:

| Codebase Type | Failure Risk | Recommendation |
|---------------|--------------|----------------|
| Greenfield, single-file, simple logic | Low | AI agent can assist (human review still needed) |
| Brownfield, 2-5 files, clear dependencies | Medium | AI agent + unit tests + human coordinator |
| Legacy monolith, >10 files, technical debt | High | AI agent should be limited to well-scoped, isolated tasks (e.g., docstrings, refactor within a single class) |
| Security-critical, compliance-heavy | Very High | Avoid AI agents for code generation; use only for linting and suggestions |

### 4.2 Cost-Benefit Recalibration

- **Training cost advantage** of open‑source models (DeepSeek 20–50× cheaper) is **eroded** by low success rates on brownfield tasks.
- **Human‑in‑the‑loop** remains essential: a "pair programmer" model where agent proposes changes and a senior engineer reviews/resolves multi‑file coordination is the only viable near‑term deployment.
- **Tooling investment:** Enterprises must build robust **patch validation pipelines** (automated tests, integration checks) before accepting any AI‑generated change, adding infrastructure overhead.
- **Expected productivity gain:** Not 10× but perhaps 1.3–1.5× for well-defined tasks, zero (or negative) for complex legacy modifications.

### 4.3 Vendor Selection Criteria

When evaluating AI coding tools, demand:
- **SWE‑Bench Pro scores** (not SWE‑Bench Verified) — ask for public set results.
- **Multi-file coordination metrics** — how does the agent handle changes spanning >3 files?
- **Context management strategy** — retrieval mechanisms, windowing, summarization.
- **Tool robustness** — error handling, retry logic, dry‑run capabilities.

Avoid vendors citing only HumanEval or SWE‑Bench Verified; those are not representative of enterprise brownfield work.

---

## 5. Recommendations

### For CIOs / Engineering Leaders

1. **Pilot in low‑risk zones** first: documentation generation, simple refactors, test creation.
2. **Never deploy unassisted** — maintain mandatory human code review for all AI‑generated patches.
3. **Measure correctly:** Track *post‑merge rollback rate* and *bug introduction rate* per AI‑assisted commit vs human‑only baseline. Do not trust vendor benchmarks.
4. **Budget for validation:** Build CI gates that run full test suites on any AI‑proposed change; this is non‑negotiable.
5. **Upskill staff** in prompt engineering and trajectory supervision; AI coding agents require different workflows than traditional IDEs.

### For Tool Vendors

1. **Prioritize multi‑file coordination** — this is the biggest gap; invest in planning layers that produce atomic, cross‑file edit plans.
2. **Improve context management** — develop smarter retrievers that can identify relevant files with >90% precision in large repos.
3. **Publish SWE‑Bench Pro scores** transparently; include breakdown by file count and language.
4. **Build robust patch application** — handle partial failures, provide rollback mechanisms, validate syntax before applying.

---

## 6. Data Gaps & Uncertainties

- **Real-world enterprise data:** SWE‑Bench Pro uses public repos; performance on proprietary, highly customized enterprise stacks may be worse (due to domain-specific patterns and internal libraries).
- **Longitudinal trends:** We lack data on whether performance is improving month‑to‑month. Track quarterly SWE‑Bench Pro scores to gauge progress.
- **Cost of failure:** No published data on actual financial impact of AI‑induced bugs in production (e.g., revert cost, incident response). This is a critical gap for ROI models.
- **Human‑AI team dynamics:** Optimal ratio of engineers to AI‑assisted commits, and best review workflows, remain under‑researched.

---

## 7. Next Research Steps

1. **Survey enterprises** using AI coding agents (Meta, Microsoft, Stripe, etc.) to gather failure case studies and mitigation strategies.
2. **Track SWE‑Bench Pro monthly** — monitor if new models cross the 30% threshold; report trend curve.
3. **Analyze GitHub issues** for AI coding tools (Claude Code, Cursor, Copilot) to categorize user‑reported failure modes in production.
4. **Benchmark by codebase type** — create sub‑categories (microservices, monoliths, data pipelines) and measure performance variance.
5. **Cost of validation study** — measure CI compute and engineer time spent reviewing AI patches vs human-written code.

---

## 8. Sources

- Emergentmind: "SWE‑Bench Pro: Industrial AI Coding Benchmark" (2025‑09‑25)
- OpenReview: SWE‑Bench Pro paper abstract (2025‑10‑08)
- arXiv:2509.16941 — SWE‑Bench Pro full paper (PDF extraction partial)
- SWE‑EVO: Benchmarking Coding Agents in (arXiv:2512.18470) — 80% maintenance vs new development figure

---

*Report generated: 2026-02-16 06:10 UTC*  
*File: `research/2026-02-16-brownfield-failure-patterns.md` (drafting)*  
*Word count: ~1,450*
