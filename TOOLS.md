# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Memory System (Voyage AI)

- **Provider**: Voyage AI (voyage-4-large)
- **Current Status**: ⚠️ Rate limited on free tier (3 RPM, 10K TPM)
- **Impact**: Semantic search degraded; system falls back to grep automatically when rate-limited
- **Check status**: `quick memory-status` or `quick voyage-status`
- **To lift limits**: Add payment method in Voyage AI dashboard: <https://dashboard.voyageai.com>
- **Rate-lock**: Meta-agent skips memory reindex for 6 hours after detecting 429 errors
- **Fallback behavior**: grep-based search (`msearch`) is used automatically; no manual intervention needed
- **Reindex schedule**: Weekly on Sunday at 04:00 Asia/Bangkok (may be skipped due to rate limits)

---

### Quick Launcher Commands (`./quick <cmd>`)

Common utilities (run `./quick help` for full list):

- `dash` / `dashboard` — CLI dashboard
- `web` — Web dashboard
- `anime <cmd>` — Anime companion (search, info, top, season, upcoming)
- `selfie [caption] [rating]` — Random anime image (safe/explicit)
- `selfie-batch <count> [rating] [caption]` — Multiple images as zip
- `mem` — Show recent memories
- `search <query>` — Search memories
- `memory-status` — Memory index status
- `memory-index` — Reindex memory files
- `memory-reindex` — Force memory reindex
- `memory-reindex-check` — Check if reindex is needed
- `memory-stats` — Detailed memory statistics
- `daemons` — Show status of persistent background agents
- `quiet-hours` — Show quiet hours status
- `health` — Concise system health summary
- `holidays` — Upcoming Indonesian holidays
- `time` — Current UTC and Bangkok time
- `weather [loc]` — Get current weather (default: Bangkok) via wttr.in
- `git-status` — Brief git status
- `git-today` — Commits from today
- `git-summary` — Commit summary by prefix (dev:, content:, research:, etc.)
- `log <category> "<message>"` — Log event to memory
- `email-clean [options]` — Auto-clean Gmail (use `--execute` to apply)
- `agents [flags]` — List sessions/agents (flags passed to `openclaw sessions`)
- `downloads [--json] [--watch SECS]` — Show aria2 download progress
- `torrent-add <magnet_or_file> [rpc_secret]` — Add magnet/torrent to aria2
- `torrent-status` — Alias for downloads
- `nyaa-search <query>` — Search Sukebei.Nyaa.si
- `nyaa-top [options]` — Top torrents by seeds
- `content-latest` — Show latest content digest
- `content-index-update` — Regenerate content/INDEX.md
- `research-watchlist` — Show latest research watchlist
- `social-monitor` — Run social monitor agent (Twitter trending digest)
- `sudo-check` — Check passwordless sudo
- `log-rotate` — Rotate aria2.log if >100MB
- `updates-check` — Check pending APT updates
- `updates-apply [--dry-run|--execute]` — Apply system updates
- `cleanup-downloads [options]` — Clean old downloads (default dry-run, retain 30 days)
- `cleanup-backups [options]` — Clean old backup tarballs (default keep 1)
- `cleanup-build-archive [options]` — Prune old build directories in `builds/` (default dry-run, keep 10)
- `cleanup-agent-artifacts [options]` — Clean stale agent artifacts (respects quiet hours)
- `agent-spawn <agent-id> <task> [--daemon]` — Spawn an agent; add --daemon for persistent 24/7 loop (respects quiet hours)
- `agent-logs [name]` — Show recent agent logs (dev, content, research, builder; default all)
- `cron` — List OpenClaw cron jobs (concise)
- `cron-status` — Show status of important cron jobs (system crontab + OpenClaw)
- `cron-failures` — Show cron jobs with recent errors (consecutiveErrors > 0 or lastStatus != "ok")
- `restart-gateway` — Restart OpenClaw gateway
- `gateway-status` — Detailed gateway status (service, port, RPC)
- `gateway-info` — Gateway status + remote access setup instructions
- `gateway-watchdog` — Show gateway watchdog log (last 20 lines)
- `gateway-fix` — Fix gateway issues (stop stray processes, restart cleanly)
- `hygiene` — Workspace hygiene check (CRLF, exec bits, large files, caches)
- `validate` — Run comprehensive validation (health, memory, agents, git, cron, logs)
- `verify` — Run comprehensive workspace verification
- `setup-all` — Run all setup scripts (sudo, torrent cron) non-interactively
- `agent-manager` — Run agent-manager maintenance checks (used by cron)
- `agent-status` — Show OpenClaw cron jobs overview (next run, last status, schedule)
- `checkpoints` — Show autonomous system checkpoints (autonomous-checkpoints.json)
- `cleanup-untracked [--execute]` — List or delete untracked files (default: list; --execute to delete)
- `daily-digest [YYYY-MM-DD]` — Generate daily digest report (default: today UTC). Saves to reports/ and prints.
- `digest` — Show the latest daily digest report from reports/ (cat the most recent)
- `git-last` — Show last commit details (files changed, stats, and message)
- `meta` — Run meta-agent once (autonomous planner)
- `meta-commit` — Auto-commit meta-agent planning files (findings.md, progress.md, task_plan.md) if changed
- `meta-logs` — Show meta-agent log (memory/meta-agent.log)
- `meta-report` — Show latest meta-agent report
- `phase` — Show current autonomous phase status (from checkpoints)
- `reports` — List daily digest reports in reports/ (most recent first)
- `session-locks [--clear]` — List stale session locks (default) or clear them (--clear)
- `status` — Concise one-line system summary (disk, load, memory, gateway, agents)
- `summary` — One-line system summary (status, disk, updates, git)
- `supervisor` — Run supervisor health check (cron monitoring, gateway, disk, memory)
- `supervisor-logs` — Show supervisor log (memory/supervisor.log)
- `today` — Show files modified today across the workspace (since midnight UTC)
- `help` — Show this help message

---

### System Maintenance

- `quick updates-check`: List pending APT updates.
- `quick updates-apply [--dry-run|--execute]`: Apply updates (dry-run default).
- `quick cleanup-agent-artifacts [--execute] [--force]`: Clean stale agent artifacts.
- `quick gateway-info`: Show gateway status and remote access setup.
- `quick gateway-watchdog`: Show gateway watchdog log.
- `quick gateway-fix`: Fix gateway lock/port issues.
- `quick hygiene`: Workspace hygiene check.
- `quick cleanup-downloads [--days N] [--execute] [--verbose]`: Clean old downloads.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]`: Clean old backups.
- `quick cleanup-build-archive [--keep N] [--execute]`: Prune old builds in `builds/` (dry-run default, keep 10).
- `quick memory-reindex-check`: Check if memory reindex needed.
- `quick memory-reindex`: Force memory reindex.
- `quick cron`: List OpenClaw cron jobs.
- `quick cron-status`: Show system + OpenClaw cron status.

---

### Monitoring

- `quick health` — One-line health summary
- `quick agents` — Active sessions/agents
- `quick mem` — Recent memories
- `quick log-rotate` — Rotate aria2.log manually

---

### Notes

- All agent logs (dev-agent.log, content-agent.log, research-agent.log) are rotated automatically via `log-rotate`.
- Systemd manages OpenClaw gateway; watchdog runs every 5 min via system crontab checking port 18789.
- Memory uses Voyage FTS+ (rate-limited free tier); reindex batched.
- Quiet hours: removed system‑wide on 2026‑02‑17; all agents run 24/7.
- Voyage rate‑lock: meta‑agent skips memory reindex for 1 hour after a 429 error, reducing log spam and API load.
- **Search fallback**: `quick search` automatically falls back to `./msearch` (a grep‑based searcher over core memory files) when Voyage AI is rate‑limited or unavailable, ensuring reliability.
  - `msearch` performs case‑insensitive searches by default, matching typical user expectations.