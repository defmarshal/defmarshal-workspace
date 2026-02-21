# Long-term Memory Index

*Last updated: 2026-02-21*

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

## Recent Learnings

### 2026-02-21
- **meta-agent robustness improvement**: Fixed crash on days with zero content/research files by replacing `ls` with `find` in snapshot calculation. The `set -euo pipefail` combined with `ls` exiting non-zero on glob mismatch caused the script to abort. Using `find` (which returns 0 even with no results) prevents false failures. Commit 9519b2e. Validated via sub-agent run; meta-agent now completes successfully on empty days. Note: sequential spawning of long-running agents may still risk timeout if both need extended runtime; consider backgrounding or adjusting timeouts in future.

- **meta-agent spawn debouncing**: Added state tracking (`memory/meta-agent-state.json`) to avoid spawning content-agent and research-agent too frequently (within 30 min). Prevents redundant launches when agents haven't yet produced output, reducing system load. Implemented in workspace-builder-20260221-0100.

- **Idea executor quality validation**: Added automatic rejection of placeholder commits (e.g., only touching `quick` or no substantive changes). Validation checks for real file modifications (extensions: sh, md, ts, js, json, yaml, etc.) and minimum insertions/deletions. Rejected ideas revert the commit and mark status `rejected`. Prevents noise in git history. Additionally implemented `monthly-digest` command to aggregate daily digests into monthly reports.

- **capability-evolver first cycle**: Deployed and ran first autonomous evolution cycle (cron every 6h UTC). Detected error signals but found the issue (missing evolver-cycle.sh) already fixed. Instead of code changes, produced a skill assessment (`skills-assessment-2026-02-21.md`) that identified duplicates and low-value skills. This analysis directly informed later skill consolidation (removed `anime-lookup`, `fivem-dev`, `clawaifu-selfie`). Validated GEP protocol compliance, gene selection, and bridge execution. Outcome: successful cycle with valuable analytical output even when no patch needed. Evolution artifacts stored in `memory/evolution/`.

### 2026-02-19
- **Token optimization trial and revert**: Added `--max-tokens` flags and conciseness directives to agent cycles to reduce token usage. Changes initially committed but immediately reverted due to output failures (truncated/incomplete results). System self‑corrected via automated revert. Lesson: aggressive token caps can break agent output; use only gentle constraints and validate thoroughly before global rollout. Added comprehensive notes to `lessons.md` under "Token Optimization" section.

### 2026-02-18
- **agent-manager git auto-commit bug fixed**: The original condition `if ! git diff --quiet && ! git diff --cached --quiet` missed untracked files, causing auto-commit to skip when only untracked files existed (e.g., reports/). Fixed by replacing with `changes=$(git status --porcelain | wc -l); if [ "$changes" -gt 0 ]; then ...`. Now correctly detects any uncommitted changes including untracked files. Validated: manual run successfully auto-committed the daily digest report.
- **quick launcher syntax error fixed + meta-agent refactor**: The `feedback)` case was misplaced after `esac` causing a parse error. Fixed by moving it inside the case block. Validated `./quick help` works. Also accepted major `agents/meta-agent.sh` refactor (simplified, deduped safety/feedback code, added create_* functions). Enforced active-tasks.md 2KB limit: pruned stale validated entry and added completed record.
