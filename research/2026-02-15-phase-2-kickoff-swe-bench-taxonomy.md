# Phase 2 Kickoff: SWE-Bench Failure Taxonomy & Agent Architecture Insights (2026-02-15 13:15 UTC)
**Research‑agent Phase 2 initial report** • Filling critical gaps

---

## 🎯 Mission

Address **Gap #1 (SWE‑Bench failure taxonomy)** from the Phase 1 watchlist. We needed to understand *why* models fail on brownfield tasks: is it ambiguity, multi‑file coordination, legacy integration, or test environment issues?

**Answer:** It's primarily **retrieval + context** problems, compounded by agent architecture.

---

## 🔬 Fresh Evidence (Fetched 2026‑02‑15 13:15 UTC)

### 1. Augment Code's SWE‑Bench Pro Analysis

**Source:** https://www.augmentcode.com/blog/auggie-tops-swe-bench-pro

**Key results:**
- Auggie (using Claude Opus 4.5) scored **51.80%** on SWE‑Bench Pro (731 problems) — highest of any agent tested
- Cursor and Claude Code, *using the exact same model*, scored lower: Auggie solved 15–17 more problems than them
- Scale's own leaderboard shows Claude Opus 4.5 at 45.89% (via SWE‑Agent scaffold)

**Critical insight:** The performance gap comes from **agent architecture**, not model weights.

### 2. Why SWE‑Bench Pro is Harder (per Augment)

- **Multi‑file edits:** Average solution touches 4.1 files, changes 107 LOC. Grep can't solve this.
- **Multiple languages:** Includes Go, TypeScript, JavaScript beyond Python. Each has distinct failure modes (terse Go errors, TypeScript type/runtime mismatches).
- **Real task diversity:** Bug fixes, features, security patches, performance optimizations, UI changes — not just "fix failing test."
- **Context retrieval:** Agents must find relevant code across large repos; failures happen when they retrieve less useful context more often.

Quote from Augment:
> "The difference comes down to what context the agent sees before it starts writing code. SWE‑bench Pro problems require understanding code that isn't in the immediate file. The agent has to find it, and finding the right code in a large repository is a retrieval problem."

### 3. GitHub AI‑Agent‑Benchmark (murataslan1)

**Source:** https://github.com/murataslan1/ai-agent-benchmark (December 2025 – January 2026, 140+ verified sources)

**Real‑world performance matrix** (user‑reported success rates):

| Agent | Multi‑File Refactor | Large Codebase (>50K LOC) | Speed | Cost/Month |
|-------|-------------------|--------------------------|-------|------------|
| Claude Code | 85–95% | 75% | Slow (30s–2m) | $100+ |
| Aider | 85–90% | 80% | Fast (3–8s) | $50–100 |
| Cursor | 70–80% | 60% | Fast (3–10s) | $20–40 |
| Windsurf | 75–85% | 70% | Moderate (5–15s) | $15 |
| Cline | 70–80% | 65% | Moderate (5–15s) | BYOK |
| Copilot Agent | 45–55% | 40% | Moderate (10–20s) | $10–39 |

**Domain‑specific performance:**
- Rust/C++: DeepSeek V3 excels
- Kotlin/Go: Minimax M2.1 (polyglot specialist)
- Swift/SwiftUI: **All models hallucinate** deprecated APIs → HIGH RISK
- Data Science: Use IDE → paste to Notebook (in‑notebook agents buggy)

**Critical issues (last 30 days):**
- Claude Code: Terminal freezing
- Cursor: Pricing opacity, overage shock
- Windsurf: "Infinite Loop" bug
- GPT‑5.2: "Breaking all the code" on simple UI requests
- Gemini 2.0 Pro: Quick derailment

---

## 🗂️ Failure Taxonomy (SWE‑Bench Pro)

Based on the evidence, here are the primary failure modes:

| Category | Description | Examples | Mitigation |
|----------|-------------|----------|------------|
| **Context Retrieval** | Agent cannot locate the correct code across large repo; retrieves top‑level APIs but misses low‑level utilities. | BCrypt fix in Ansible spans layers; grep finds high‑level APIs but utility function needed. | Semantic code indexing (Augment Context Engine, MCP servers, custom index). |
| **Multi‑File Coordination** | Solutions need 4+ files; agents often modify one file and miss ripple effects. | Changing a function signature requires updates in 5 call sites across different modules. | Two‑tier workflow (plan mode → then generate), explicit dependency mapping. |
| **Language‑Specific Quirks** | Go terse errors; TypeScript type/runtime mismatch; polyglot repos confuse agents. | TypeScript compile passes but runtime fails; Go errors not actionable for LLM. | Domain‑specific MCPs, language‑specialized models (Minimax for Kotlin/Go, DeepSeek for Rust/C++). |
| **Context Window Degradation** | Long contexts (>100K tokens) cause reasoning derailment; model forgets earlier constraints. | Gemini 2.0 Flash (1M context) derails quickly; Opus 4.5 also affected. | RAG with chunking, plan mode to condense understanding, smaller focused contexts. |
| **Infinite Loops / Spirals** | Agent gets stuck in clarification questions or repeated failed attempts. | Windsurf "Infinite Loop" bug; Cursor over‑searching. | Turn limits, cost caps, human‑in‑the‑loop stopgaps. |
| **Test Environment Flakiness** | SWE‑Bench Pro uses reproducible Docker; agents fail due to environment mismatches not code errors. | Dependencies missing in container; tests depend on external services. | Better harness, pre‑built containers, agent awareness of environment. |
| **Benchmark Overfitting** | Models trained on SWE‑Bench Verified (greenfield) struggle on Pro (brownfield) because they've memorized patterns. | GPT‑5.2 "Death by Benchmark" — excellent on leaderboards, poor in real use. | Use contamination‑resistant benchmarks (GPL repos, private codebases). |

---

## 💡 Strategic Implications for Enterprises

1. **Don't trust greenfield scores** for brownfield work. A model with 80% SWE‑Bench Verified may deliver <25% on your legacy codebase.
2. **Invest in retrieval infrastructure.** Semantic code indexing (like Augment's Context Engine or custom MCP) can add ~6 points to success rates (45% → 51%).
3. **Use specialized models per language.** DeepSeek for Rust/C++, Minimax for Kotlin/Go, Claude for Python/JS.
4. **Adopt "Plan Mode" explicitly.** Force agents to output an architecture plan before coding; reduces loop count and context drift.
5. **Two‑tier workflow:** Expensive models (Opus) for planning only; cheap models (DeepSeek, Minimax) for code generation.
6. **Expect and budget for human review.** Even best agents: 15–20% failure on multi‑file refactors in large codebases.
7. **Security vigilance:** AI hallucinates packages (zeta‑decoder attack vector). Verify every dependency manually.

---

## 📊 Updated Gap Status (Post‑Fetch)

| Gap | Priority | Status | Evidence Gathered |
|-----|----------|--------|-------------------|
| 1. SWE‑Bench failure taxonomy | 🔴 CRITICAL | **Partially filled** | Augment analysis + GitHub benchmark provides clear taxonomy (retrieval, multi‑file, language quirks, context degradation, infinite loops, test env, overfitting) |
| 2. Data center power constraints | 🔴 CRITICAL | Not started | Need CAISO/ERCOT filings, DOE studies |
| 3. CBDC live transaction volumes | 🔴 CRITICAL | Partial URLs broken | Need direct central bank reports (PBOC, ECB, BoE) |
| 4. Blackwell real‑world performance | 🔴 CRITICAL | Stalled (MLPerf 404) | Try alternative news/analyst coverage (The Next Platform, Analytics India Magazine) |
| 5. Anime Q4 2025 earnings | 🟠 HIGH | Not started | Wait for Sony/Netflix/Disney+ Q4 results |
| 6. Open‑source cost curves | 🟠 HIGH | Not started | Monthly leaderboard tracking needed |
| 7. AI safety incidents | 🟡 MEDIUM | Not started | aiincidents.org, NIST reports |

**Next actions (Sprint 1):**
- Attempt Blackwell performance via news sources (avoid MLPerf 404)
- Start data center power constraints research
- Begin CBDC volumes via central bank publications

---

## 📝 Report Metadata

- **Filename:** `2026-02-15-phase-2-kickoff-swe-bench-taxonomy.md`
- **Size:** ~5 KB
- **Status:** Ready to commit
- **Sources cited:** Augment Code blog, GitHub ai‑agent‑benchmark repo (140+ sources)

---

**Research‑agent signing off before quiet hours, nya~! (◕‿◕)♡**

*We've turned a critical gap into actionable intelligence. Phase 2 underway.*
