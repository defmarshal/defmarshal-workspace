# Long-term Memory Index

*Last updated: 2026-03-04*

## Personal
def, UTC+7, mewmew assistant; anime, tech

## Projects
Memory System, Workspace Health & Automation, Idea pipeline, openclaw-idle-rpg, Research Hub, Torrent System

## Links
- `active-tasks.md` (current work)
- `memory/YYYY-MM-DD.md` (daily logs)
- `lessons.md` (patterns)
- `TOOLS.md` (config)
- `CRON_JOBS.md` (schedules)

## Resources
- Voyage AI: https://dashboard.voyageai.com
- OpenClaw: https://docs.openclaw.ai
- GitHub: defmarshal/defmarshal-workspace

## Notes
- Gateway: port 18789; Memory: local FTS+ only (Voyage disabled); systemd linger recommended: `sudo loginctl enable-linger ubuntu`
## Learnings (latest)
- 2026-03-04: LinkedIn PA agent cron stuck with stale `runningAtMs` flag causing missed runs. Recovery: manually executed agent script, then reset cron state via disable/enable cycle. Also removed duplicate cron job entry to prevent future confusion. Lesson: Cron state may become stale; a simple disable/enable clears `runningAtMs` and resets schedule. Consider investigating root cause (race condition on completion signal).
- 2026-03-03: Fixed dashboard cron by switching OpenClaw `dashboard-data-updater` payload to `./scripts/generate-dashboard-data.sh`. This ensures correct data: `disk_history` (24-value sparkline) and agent status (`name`, `active`, `last_run`, `last_line`). The previous Python script produced empty fields and misaligned schema.
- 2026-03-03: Meta-agent skill installation updated: changed from `openclaw skills install` (removed CLI) to `openclaw plugins install`. Detected weather skill request but weather functionality is provided by `quick weather` (wttr.in), not a plugin. Heuristic to avoid installing non-existent plugins needs refinement. Lesson: verify plugin availability before attempting install; align tool invocation with current CLI version.
- 2026-03-02: Added observability: quick idea-health command monitors autonomous idea pipeline health (generator/executor status, pending ideas, error tail). Demonstrates incremental monitoring improvements for self-directed systems.
- 2026-03-02: Dashboard data updater cron job was undocumented and had Python deprecation warnings. Fixed: added to CRON_JOBS.md; replaced datetime.utcnow() with timezone-aware datetime.now(UTC); verified script runs cleanly. Lesson: Regularly audit cron jobs against documentation; proactively fix deprecation warnings to avoid future breakage.
- 2026-03-01: Workspace-builder closure integrity — ensure all generated outputs (planning docs, agent summaries, daily digest updates) are committed before marking validated; untracked files create audit gaps. Fixed: remediation commit added missing artifacts and corrected verification metrics. Lesson: verify `git status` allows only expected state file modifications (e.g., disk-history.json) before final close.
- 2026-02-23: Idea generator overhaul (slug deduplication, substantive file creation via printf, reliable executor validation) and notifier agent fix (log function, OpenClaw JSON filtering); executor bug: replaced heredoc with printf.
- 2026-02-24: Meta-agent cron duplication bug fixed: added JSON filtering (sed -n '/^{/,$p') before jq in all cron checks; corrected git-janitor-cron schedule from hourly (`15 * * * *`) to every 6 hours (`0 */6 * * *`) per CRON_JOBS.md; cleaned up duplicate cron entries, preventing uncontrolled accumulation. Plus: automated stale idea branch cleanup in git-janitor (merge-check, age threshold, safe arithmetic) with self-correction of merge-base logic. Additionally: workspace-builder applied 17 security updates and validated system health (disk 67%, gateway healthy, memory clean).
- 2026-02-25: Workspace-builder refined maintenance patterns: phased APT updates override; active-tasks.md pruning to <2KB; systematic stale idea branch cleanup; push-pending-first pattern; implemented `quick validate-constraints` command for proactive enforcement. System health consistently green.
- 2026-02-28: Enhanced constraints: added shebang validation for scripts/*.sh; automated archival of completed active-tasks entries to daily logs; refined dashboard data commit hygiene; all systems green.

- 2026-02-22: Autonomous idea pipeline: generator (6h UTC) proposes, executor (2h UTC) implements; validation rejects placeholder commits (≥5 lines, substantive changes).
