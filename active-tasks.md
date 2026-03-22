# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-22 08:15 UTC**

System status: Stable. Disk usage ~82%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Fix confirmed working! Mar 21 12:14 UTC run completed successfully with no hangs. Processed 1 page, labeling ~100+ emails across 42+ Sweep categories. The timeout changes (curl 10s connect / 60s max, 70s subprocess) resolved the instability. Monitoring continues but stability looks good.

**Shared Seed Pool** (used by Research, Content, and Code Gardeners):
- Total seeds: 1222
- Processed seeds: 398
- Remaining: 824
At current hourly frequency per gardener, backlog will clear in ~35 days. Consider batch increases during Nyepi if throughput needs to accelerate.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Gardeners Status:**
- **Research Gardener** (cron research-gardener-1773046574): Last run 00:15 UTC (processed "It's been 20 years since the first tweet"). Tavily API not set; using local synthesis. Reports: 456 total.
- **Content Gardener** (cron content-gardener-XXXXX): Last seen Mar 22 02:15 UTC (processed "Planner suggestion: starlink v2 launch schedule"). Producing blog-style content with OpenRouter fallback. Content output: 783+ files (4 new today). Running normally during Nyepi period.
- **Code Gardener** (cron code-gardener-1773047374): Last seen Mar 21 19:08 UTC. Generating Python apps via enhanced fallback (OpenRouter instability). Apps count: ~1600+.

All gardeners operate on shared seed pool with cooperative allocation; no duplicate work (tracked in `memory/processed_seeds.jsonl`).
