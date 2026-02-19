# Research Plan: Continuous Domain Analysis (Anime, Banking, Tech, AI)

**Date:** 2026-02-19
**Agent:** research-agent
**Goal:** Conduct comprehensive research across four key domains: anime, banking, tech, and AI. Gather latest trends, market data, notable developments, and future outlooks.

---

## Research Strategy

### Phase 1: Information Gathering (Web Search + Fetch)
For each domain, perform targeted searches to collect:
- Latest news and trends (last 3-6 months)
- Market statistics and forecasts
- Notable product/service releases
- Emerging technologies or platforms
- Key players and competitive landscape
- Challenges and opportunities

### Phase 2: Deep Dive & Source Extraction
For promising results, use web_fetch to extract detailed content from authoritative sources (industry reports, official announcements, reputable news outlets).

### Phase 3: Synthesis & Reporting
Create structured markdown reports for each domain with:
- Executive summary
- Current landscape
- Key trends & statistics
- Notable developments
- Future outlook
- Sources cited

### Phase 4: Cross-Domain Analysis
Identify intersections and macro-trends affecting multiple domains.

---

## Execution Order

1. **Anime Industry** – streaming wars, market growth, production trends, global expansion
2. **Banking Sector** – AI adoption, fintech disruption, regulatory changes, customer experience
3. **Technology** – AI hardware, semiconductor trends, open-source frameworks, deployment patterns
4. **AI Developments** – new models, agentic systems, cost trajectories, enterprise adoption

---

## Success Criteria

- Four detailed research reports created in `research/` with date-prefixed filenames
- Each report 1-3 KB with sourced information
- Summary output highlighting key findings across all domains
- All content committed to git

---

## Notes

- Use Brave search via `web_search` (provider: Brave API)
- Fetch full content when snippets indicate valuable data
- Prioritize recent sources (2025-2026)
- Focus on quantitative data where available (market sizes, adoption rates, etc.)
