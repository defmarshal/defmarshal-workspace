# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-21 02:15 UTC**

System status: Stable. Disk usage ~82%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: ✅ Fix confirmed working! Mar 21 12:14 UTC run completed successfully with no hangs. Processed 1 page, labeling ~100+ emails across 42+ Sweep categories. The timeout changes (curl 10s connect / 60s max, 70s subprocess) resolved the instability. Monitoring continues but stability looks good.

**Backlog:** 810 unprocessed seeds remaining in `memory/seeds.jsonl` (1152 total, 342 processed). At 1 seed per run, clearing backlog would take ~33 days at hourly frequency. Consider increasing frequency or batch processing.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Code gardener** (cron code-gardener-1773047374): Running continuously throughout Mar 21 UTC. Current run started at 22:06 UTC. Processed seeds using enhanced fallback (OpenRouter returning length 0). Status: 395 seeds processed, 1607 apps generated. Remaining backlog: ~817 seeds (1212 total seeds - 395 processed). Process PID 438081 active. Enhanced fallback scripts working reliably despite OpenRouter instability.

**Content gardener** (cron 1773046735, manual recovery 21 Mar 19:05 UTC): Completed run - processed seed "Towards Differentiating Between Failures and Domain Shifts in Industrial Data Streams". Output written successfully. Cleared stale cron runningAtMs state.
