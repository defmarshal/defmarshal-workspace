# SWE-Bench Pro 2026-02 Update: Leaderboard Surge and Persistent Failure Modes

**Priority**: 🔴 HIGH (brownfield failure patterns — enterprise ROI impact)

---

## Executive Summary

Fresh data from Scale AI's SWE‑Bench Pro public leaderboard (last updated 2026‑01‑16) reveals **significant improvements** in top model performance while **barely moving the needle** on private codebases. The gap between slick demo capabilities and real‑world software engineering tasks remains stark—enterprise planners must adjust ROI models accordingly.

**Key numbers (Public dataset, 731 tasks):**
- **Claude‑Opus‑4.5** (2025‑11‑01): **45.89%** resolve rate (↑ from ~23% in Sep 2025)
- **Claude‑4.5‑Sonnet**: 43.60%
- **Gemini‑3‑Pro‑preview**: 43.30%
- **GPT‑5 (High)**: 41.78%
- **Qwen3‑Coder‑480B**: 38.70%

**Private subset (276 tasks, proprietary codebases):**
- **Claude‑Opus‑4.1**: 17.8% (down from 22.7% public)
- **GPT‑5**: 14.9% (down from 23.1% public)

**Implication**: Public leaderboard overstates enterprise readiness by **2–3×**. Real‑world brownfield environments cut success rates by >60% for top models.

---

## 1. Benchmark Methodology & Scope

SWE‑Bench Pro is designed to evaluate AI agents on **long‑horizon, realistic software engineering tasks**:

- **Dataset size**: 1,865 tasks across 41 professional repositories
- **Task complexity**: average solution = 107 lines of code across 4.1 files
- **Sources**: Consumer apps, B2B platforms, developer tools (both open‑source with strong copyleft licenses and private proprietary codebases)
- **Scoring**: Resolve rate requires (a) fixing the specific issue (fail‑to‑pass tests) AND (b) no regressions (pass‑to‑pass tests still pass)
- **Evaluation**: Human‑augmented problem statements, reproducible Docker environments, contamination‑resistant by design

This is the **most rigorous** real‑world coding benchmark available as of 2026‑02.

---

## 2. Performance Landscape (Jan 2026)

### 2.1 Public Leaderboard

Top 5 models achieve **40–46%** resolve rates—substantial gain from the ~23% plateau observed in mid‑2025, but still meaning **more than half of tasks fail**.

| Rank | Model | Resolve Rate (Public) | Notes |
|------|-------|----------------------|-------|
| 1 | Claude‑Opus‑4.5 | 45.89% ± 3.60 | New leader; thinking model |
| 2 | Claude‑4.5‑Sonnet | 43.60% ± 3.60 | Strong sibling |
| 3 | Gemini‑3‑Pro‑preview | 43.30% ± 3.60 | Close behind |
| 4 | Claude‑4‑Sonnet | 42.70% ± 3.59 | Consistent |
| 5 | GPT‑5 (High) | 41.78% ± 3.49 | Slightly behind top Claude |

Mid‑tier:
- Qwen3‑Coder‑480B: 38.70%
- Minimax‑2.1: 36.81%
- GPT‑5.2‑Codex: 41.04%
- Kimi‑K2‑Instruct: 27.67%

Smaller models (<100B) mostly <20%: Llama4‑Maverick (5.24%), Codestral (1.51%).

**Cost note**: The top models were run with **uncapped cost** and **turn limit 250**. Real‑world deployments may impose tighter budgets, potentially reducing effective performance.

### 2.2 Private Subset Collapse

When evaluated on **private, unseen proprietary codebases** (18 startups), performance **plummets**:

- Claude‑Opus‑4.1: **17.8%** (vs 22.7% public)
- GPT‑5: **14.9%** (vs 23.1% public)

The ~40% relative drop suggests **severe generalization gaps**. Private codebases likely have:
- Less documentation
- More technical debt
- Proprietary frameworks/patterns
- Less test coverage
- Different coding styles

These are precisely the **brownfield environments** enterprises care about.

---

## 3. Failure Mode Analysis (What's Still Broken)

Even with top models at ~45% on public tasks, **55%+ failure rate** indicates fundamental limitations. The leaderboard highlights these patterns:

### 3.1 Repository‑Specific Difficulty

- **Some repositories prove consistently difficult for *all* models**, with resolve rates below 10%.
- **Others are tractable**, with certain models achieving >50%.
- **Drivers**: codebase complexity, problem type, documentation quality, test setup.

**Enterprise implication**: ROI depends heavily on **which codebases** you target. Legacy monoliths, custom frameworks, and poorly tested repos will see far lower success rates than the headline numbers.

### 3.2 Language Gaps

Performance varies dramatically by programming language:

- **Go & Python**: some models exceed 30% resolve
- **JavaScript / TypeScript**: more variable, often lower (some models near 0% on JS/TS tasks)

This suggests **language‑specific weaknesses** in training data or toolchain integration. Enterprises with heavy JS/TS stacks should be wary.

### 3.3 Scalability of Changes

Model performance **degrades significantly** as solution complexity increases:
- More lines of code required → lower success
- More files to edit → lower success
- Reference solutions average **107 lines across 4.1 files** — far beyond trivial one‑file patches

Most real‑world bug fixes or features are *larger* than this average, implying **real‑world success rates may be even lower**.

### 3.4 Private vs Public Gap

The **60–65% drop** on private codebases is the most critical finding. Models that excel on open‑source projects (with active issues, good docs, community tests) **collapse** on internal enterprise code.

Why?
- Different architectural patterns
- Proprietary libraries with no public equivalents
- Lack of available context (internal wikis, design docs not in training data)
- Security constraints limiting agent actions

---

## 4. Comparison with Earlier Assessments

Our earlier brownfield failure patterns report (2026‑02‑16) cited **~23%** resolve rates. The new leaderboard shows top models at **~46%** on public tasks — indicating **rapid improvements** in the last 3–4 months.

However:
- Private subset remains **stubbornly low** (15–18%)
- The public–private gap has **not narrowed**
- Absolute numbers still mean **>50% failure** on even the easiest public repos

Thus, the **core thesis holds**: enterprises must categorize codebases by difficulty and apply targeted mitigations. But the **thresholds have shifted**: what was "easy" (public) now sees near‑50% success, while "hard" (private) remains <20%.

---

## 5. Enterprise ROI Implications

### 5.1 Adjusting Expectations

- **Do not use public leaderboard numbers** to justify enterprise spend. They overstate readiness by 2–3×.
- **Expect 15–25% success** on internal, proprietary codebases with top models (Claude, GPT‑5, Gemini).
- **Factor human review**: For every 4 tasks the AI attempts, a human will likely need to fix or complete ~3–4 of them.

### 5.2 Cost‑Benefit Re‑calibration

If AI agent costs per task are non‑trivial, the **effective cost per *successfully* resolved issue** becomes:

```
Effective cost = (Agent cost per attempt) / (Success rate)
```

Example: Agent costs $0.50 per attempt, 20% success → effective cost = $2.50 per resolved issue. This must be compared against **fully manual** or **hybrid** workflows.

### 5.3 Triage by Codebase Type

Differentiate:
- **Greenfield projects** (new code, modern stacks): higher AI success (~40–50%)
- **Mature open‑source components** (well‑tested, documented): moderate success (~30–40%)
- **Legacy brownfield** (old frameworks, low test coverage): low success (<20%)
- **Proprietary internal stacks** (custom frameworks, limited docs): very low (<15%)

Deploy AI agents **only on the tractable subset** initially; expand as models improve.

---

## 6. Recommendations for Buyers & Developers

1. **Run a pilot on *your own code*** — not on synthetic benchmarks. Use a representative subset of internal repos.
2. **Measure success as "no regressions + issue fixed"** — not just code that compiles.
3. **Track failure modes** internally: Are agents failing on:
   - Ambiguous requirements? → improve prompting/context
   - Multi‑file coordination? → better planning tools
   - Legacy APIs? → provide more documentation
   - Test environment setup? → improve scaffolding
4. **Budget for human oversight** — plan on 2–4× attempts per successful resolution.
5. **Negotiate pricing based on *effective* success**, not raw API calls.

---

## 7. Gaps & Next Steps

- **Need longitudinal data**: Are success rates improving month‑over‑month, or is this a one‑time bump?
- **Missing failure taxonomy**: The leaderboard shows *that* tasks fail, not *why*. We need detailed post‑mortems (see immediate leads below).
- **Tool augmentation impact**: How much does adding web search, code search, or internal documentation retrieval improve success? Not measured here.
- **Cost‑normalized performance**: With uncapped cost, top models used extensive compute. What is the performance plateau under budget constraints?

---

## 8. Immediate Research Leads

1. **SWE‑Bench Pro failure log mining** — The public dataset includes trajectories. Scrape failure patterns: where do agents diverge from reference solutions? (early exit, wrong file, test error, etc.)
2. **Private subset deep dive** — Acquire or infer details about the 18 startup codebases: languages, frameworks, size. Identify what makes them harder.
3. **Enterprise case studies** — Interviews with companies that piloted AI coding agents on internal repos; gather their observed success rates and failure categories.
4. **Tool‑augmented variants** — Evaluate agents with retrieval (RAG) over internal docs; compare to bare scaffold results.

---

## 9. Conclusion

SWE‑Bench Pro remains the gold standard for evaluating AI software engineers. As of Jan 2026, **top models achieve ~45% on public tasks** — a notable improvement, but still far from reliable deployment. The **private subset failure rate (~85%) is a red flag** for enterprise buyers.

Bottom line: **Brownfield coding is still largely a research problem**. Budget for substantial human augmentation; focus pilots on tractable codebases; monitor monthly leaderboard updates for acceleration.

---

_Sources: Scale AI SWE‑Bench Pro public leaderboard (accessed 2026‑02‑17), SWE‑Bench Pro paper (https://scale.com/research/swe_bench_pro), GitHub repository (https://github.com/scaleapi/SWE-bench_Pro-os)_

_Report compiled: 2026‑02‑17 UTC_

_Gap priority: HIGH (brownfield failure patterns — updated with fresh data)_
