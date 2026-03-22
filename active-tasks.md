# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-22 08:15 UTC**

System status: Stable. Disk usage ~82%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Fix confirmed working! Mar 21 12:14 UTC run completed successfully. Currently running (cron-triggered 2026-03-22 21:06 UTC, BATCH_SIZE=100, PAGES_PER_RUN=1). Processed 1 page, labeling ~100+ emails across 42+ Sweep categories. The timeout changes (curl 10s connect / 60s max, 70s subprocess) resolved the instability. Stability looks good.

**Shared Seed Pool** (used by Research, Content, and Code Gardeners):
- Total seeds: 1222
- Processed seeds: 433 (35.4%)
- Remaining: 789
At current hourly frequency per gardener, backlog will clear in ~33 days. Consider batch increases during Nyepi if throughput needs to accelerate.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Gardeners Status:**
- **Research Gardener** (cron research-gardener-1773046574): Last run 22 Mar 23:03 UTC (processed "Publisher pulls horror novel ‘Shy Girl’ over AI concerns"). Tavily API not set; using local synthesis. Reports: 456+ total. Backlog: 789/1222 seeds remaining (~33 days at current rate).
- **Content Gardener** (cron content-gardener-1773046735): Last successful run 22 Mar 20:09 UTC (content written). **Cron at 23:03 UTC failed** — API rate limit reached. No content produced in ~3 hours. Needs attention: OpenRouter quota or rate limit mitigation.
- **Code Gardener** (cron code-gardener-1773047374): Last seen Mar 21 21:08 UTC. Generating Python apps via enhanced fallback (OpenRouter instability). Apps count: ~1600+.

All gardeners operate on shared seed pool with cooperative allocation; no duplicate work (tracked in `memory/processed_seeds.jsonl`).
