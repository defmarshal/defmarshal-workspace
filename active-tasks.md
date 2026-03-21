# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-21 02:15 UTC**

System status: Stable. Disk usage ~82%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Fix confirmed working! Mar 21 12:14 UTC run completed successfully with no hangs. Processed 1 page, labeling ~100+ emails across 42+ Sweep categories. The timeout changes (curl 10s connect / 60s max, 70s subprocess) resolved the instability. Monitoring continues but stability looks good.

**Backlog:** 810 unprocessed seeds remaining in `memory/seeds.jsonl` (1152 total, 342 processed). At 1 seed per run, clearing backlog would take ~33 days at hourly frequency. Consider increasing frequency or batch processing.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Code gardener** (cron code-gardener-1773047374): Completed 21 Mar 01:18 UTC (processed seed: Multi-Trait Subspace Steering to Reveal the Dark Side of Human-AI Interaction). Used enhanced fallback (OpenRouter returned length 0). Remaining backlog: ~490 seeds. Next run scheduled ~01:23 UTC. Issues: OpenRouter instability; fallback scripts working.

**Content gardener** (cron 1773046735, manual recovery 21 Mar 19:05 UTC): Just launched after stale cron state detection. Processing seeds from backlog. Status: running (PID 416372).
