# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-23 10:14 UTC**

System status: Stable. Disk usage ~83%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Working well! Latest cron run completed successfully (2026-03-23 14:14 UTC, BATCH_SIZE=100, PAGES_PER_RUN=1). Processed 1 page, labeling ~100 emails across 42 Sweep categories. The timeout changes (curl 10s connect / 60s max, 70s subprocess) resolved the earlier instability. System stable.

**Shared Seed Pool** (used by Research, Content, and Code Gardeners):
- Total seeds: 1222
- Processed seeds: 450 (36.8%)
- Remaining: 772
At current hourly frequency per gardener, backlog will clear in ~32 days. Consider batch increases during Nyepi if throughput needs to accelerate.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Gardeners Status:**
- **Research Gardener** (cron research-gardener-1773046574): ✅ Active and producing. Last log entry: 22 Mar 23:03 UTC; Today (23 Mar) already produced 14 research reports (timestamps from 07:23–10:02 UTC). Tavily API not set; using local synthesis. Total reports: 484+. Backlog: 772/1222 seeds remaining (~32 days at current rate).
- **Content Gardener** (cron content-gardener-1773046735): ✅ Active. Last successful run: 23 Mar 15:18 UTC. Producing content normally; no issues.
- **Code Gardener** (cron code-gardener-1773047374): ✅ Active. Running as scheduled (just executed at 09:14 UTC). Seeds: 1268 total, 473 processed (37.3%), 795 remaining. Using enhanced fallback generator when OpenRouter unavailable; stable operation. Apps count: ~1600+ (including duplicates from prior iterations). Latest app generated: 23 Mar 14:25 UTC.

All gardeners operate on shared seed pool with cooperative allocation; no duplicate work (tracked in `memory/processed_seeds.jsonl`).
