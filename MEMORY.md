# Long-term Memory Index

*Last updated: 2026-02-27*

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
- 2026-02-23: Idea generator overhaul (slug deduplication, substantive file creation via printf, reliable executor validation) and notifier agent fix (log function, OpenClaw JSON filtering); executor bug: replaced heredoc with printf.
- 2026-02-24: Meta-agent cron duplication bug fixed: added JSON filtering (sed -n '/^{/,$p') before jq in all cron checks; corrected git-janitor-cron schedule from hourly (`15 * * * *`) to every 6 hours (`0 */6 * * *`) per CRON_JOBS.md; cleaned up duplicate cron entries, preventing uncontrolled accumulation. Plus: automated stale idea branch cleanup in git-janitor (merge-check, age threshold, safe arithmetic) with self-correction of merge-base logic. Additionally: workspace-builder applied 17 security updates and validated system health (disk 67%, gateway healthy, memory clean).
- 2026-02-25: Workspace-builder refined maintenance patterns: phased APT updates override; active-tasks.md pruning to <2KB; systematic stale idea branch cleanup; push-pending-first pattern; implemented `quick validate-constraints` command for proactive enforcement. System health consistently green.
- 2026-02-22: Autonomous idea pipeline: generator (6h UTC) proposes, executor (2h UTC) implements; validation rejects placeholder commits (≥5 lines, substantive changes).
