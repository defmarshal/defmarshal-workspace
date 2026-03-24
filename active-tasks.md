# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-24 13:25 UTC**

System status: Stable. Disk usage ~83%. Git janitor cron executed but died silently; manual recovery performed (see details below).

**Meta-Summary Cron**: Currently executing (2026-03-24 13:25 UTC) — gathering system metrics and sending Telegram summary.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Working well! Latest cron run completed successfully (2026-03-24 00:08 UTC, BATCH_SIZE=100, PAGES_PER_RUN=1). Processed 1 page, labeling emails across 42+ Sweep categories. System stable.

**Shared Seed Pool** (used by Research, Content, and Code Gardeners):
- Total seeds: 1368
- Processed seeds: 549 (40.1%)
- Remaining: 819
At current **1 seed per run** frequency (hourly), backlog will clear in ~11 days. **Throughput bottleneck identified: gardeners process only one seed per execution.** To accelerate, we will either increase batch size or cron frequency.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Gardeners Status (2026-03-24):**
- **Research Gardener** (cron research-gardener-1773046574): ✅ Active. Producing ~1 report/hour. Today so far: 23 research reports (latest 13:04 UTC). Tavily API not set; using local synthesis. Total reports: 500+.
- **Content Gardener** (cron content-gardener-1773046735): ✅ Active. Producing ~1 report/hour. Today so far: 11 content reports (latest 13:01 UTC). No issues.
- **Code Gardener** (cron code-gardener-1773047374): ✅ Active but **slow**. Agent calls often time out (60s) -> uses enhanced fallback. Today so far: at least 6 apps generated (latest 13:18 UTC). No crashes observed; running normally now.

**Issues & Actions:**
- **Git janitor cron (06:12 UTC) died without logging.** Manual run completed successfully, committing pending gardener changes (5 files). Root cause unknown (possible transient lock or env). Will monitor.
- **Gardeners throughput**: Single-seed-per-run limits output. Plan: **increase batch size to 5 seeds/run** (with file locking) or **increase cron frequency to every 15 min**. Will implement batch-processing with `fcntl` lock on `memory/gardeners.lock` to avoid race conditions and safely boost throughput 5×.
- **Code gardener agent timeout** may be reduced to 30s to cut worst-case latency.

All gardeners operate on shared seed pool with cooperative allocation; processed seeds tracked in `memory/processed_seeds.jsonl`. No duplicate work observed.
