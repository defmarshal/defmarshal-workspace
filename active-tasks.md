# Active Tasks Registry

**Current active tasks - UPDATED 2026-03-20 16:13 UTC**

System status: Stable. Disk usage ~82%. Nyepi holiday period active (Mar 18–24) — reduced agent activity expected.

Agent Manager: Running normally via cron. Maintenance checks remain active.

**Email Sweep**: Interrupted (PID 238994 exited ~19:10 UTC). Processed ~600+ labels from batch of 500 (overlap due to multiple runs). Started 19:07:50 UTC, labeled continuously until 19:10:13, then terminated without "Finished" line (possible timeout or crash). State token unchanged: 01732567249931151644. Concurrency issue: multiple overlapping runs observed (brief PIDs 239329, 239331). Recommend adding PID file lock and/or extending cron interval.

**Backlog:** 810 unprocessed seeds remaining in `memory/seeds.jsonl` (1152 total, 342 processed). At 1 seed per run, clearing backlog would take ~33 days at hourly frequency. Consider increasing frequency or batch processing.

**Memory reindex:** Rate-limited (Voyage 3 RPM free tier). Will retry automatically. 63 memory files need indexing.

**Code gardener** (cron code-gardener-1773047374): Not running (stale state). Last completed: 20 Mar 17:04 UTC (processed seed: Beyond Accuracy: An Explainability-Driven Analysis of Harmful Content Detection). Cron state `runningAtMs` remains set, blocking new runs. Agent-manager should clear it on next check (~30 min). Issues: 491 seeds remaining; many OpenRouter failures; fallback scripts used.

**Recently completed:**
- **Content gardener** (cron 1773046735, 19 Mar 20:02 UTC): Finished ~20:03 UTC. Processed 29 seeds into content posts (Mar 17–19). All content written successfully. No errors.
- **Content gardener** (cron 1773046735, 20 Mar 02:14 UTC): Finished ~02:15 UTC. Processed 1 seed (Intent Formalization). All content written successfully. No errors.

