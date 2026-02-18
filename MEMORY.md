# Long-term Memory Index

*Last updated: 2026-02-18*

## Personal
- **Name**: def
- **Timezone**: UTC+7 (Indochina Time)
- **Assistant**: mewmew (anime girl 2000s texting style) – kawaii, enthusiastic, kaomoji, desu/nya
- **Interests**: anime, exploring new things, tech projects

## Current Projects (See projects.md for full status)
- Memory System Maintenance (Voyage AI + openclaw-memory + neural-memory)
- Workspace Health & Automation (cron agents, email cleaner, dashboard)
- Anime Companion (anime info + TTS + selfies)
- Torrent System (aria2 + nyaa integration)
- Ongoing improvements via workspace-builder

## Quick Links
- **Full history**: `MEMORY_HISTORY.md` (detailed timeline & learnings)
- **Active tasks**: `active-tasks.md`
- **Daily logs**: `memory/YYYY-MM-DD.md`
- **Lessons learned**: `lessons.md`
- **Project details**: `projects.md`
- **Tools & config**: `TOOLS.md`, `CRON_JOBS.md`

## Important Resources
- Voyage AI dashboard: https://dashboard.voyageai.com
- OpenClaw docs: https://docs.openclaw.ai
- GitHub repo: `defmarshal/defmarshal-workspace`

## Notes
- Memory search: Voyage AI disabled; using local SQLite FTS/grep fallback. Status: `quick memory-status`
- Gateway runs on port 18789; health: `quick health` (if quick command available)
- systemd linger recommended: `sudo loginctl enable-linger ubuntu` for service persistence

## Recent Learnings (2026-02-18)
- **agent-manager git auto-commit bug fixed**: The original condition `if ! git diff --quiet && ! git diff --cached --quiet` missed untracked files, causing auto-commit to skip when only untracked files existed (e.g., reports/). Fixed by replacing with `changes=$(git status --porcelain | wc -l); if [ "$changes" -gt 0 ]; then ...`. Now correctly detects any uncommitted changes including untracked files. Validated: manual run successfully auto-committed the daily digest report.
- **quick launcher syntax error fixed + meta-agent refactor**: The `feedback)` case was misplaced after `esac` causing a parse error. Fixed by moving it inside the case block. Validated `./quick help` works. Also accepted major `agents/meta-agent.sh` refactor (simplified, deduped safety/feedback code, added create_* functions). Enforced active-tasks.md 2KB limit: pruned stale validated entry and added completed record.
