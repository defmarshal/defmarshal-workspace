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

### Quick Launcher Commands (`./quick <cmd>`)

Common utilities (run `./quick help` for full list):

- `dash` / `dashboard` — CLI dashboard
- `web` — Web dashboard
- `anime <cmd>` — Anime companion (search, info, top, season, upcoming)
- `selfie [caption] [rating]` — Random anime image (safe/explicit)
- `selfie-batch <count> [rating] [caption]` — Multiple images as zip
- `mem` / `memory` — Show recent memories
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
- `cleanup-agent-artifacts [options]` — Clean stale agent artifacts (respects quiet hours)
- `agent-spawn <agent-id> <task>` — Spawn an agent (dev, content, research, or custom) via sessions_spawn
- `agent-logs [name]` — Show recent agent logs (dev, content, research, builder; default all)
- `cron` — List OpenClaw cron jobs (concise)
- `cron-status` — Show status of important cron jobs (system crontab + OpenClaw)
- `restart-gateway` — Restart OpenClaw gateway
- `gateway-status` — Detailed gateway status (service, port, RPC)
- `gateway-info` — Gateway status + remote access setup instructions
- `gateway-watchdog` — Show gateway watchdog log (last 20 lines)
- `gateway-fix` — Fix gateway issues (stop stray processes, restart cleanly)
- `hygiene` — Workspace hygiene check (CRLF, exec bits, large files, caches)
- `validate` — Run comprehensive validation (health, memory, agents, git, cron, logs)
- `verify` — Run comprehensive workspace verification
- `setup-all` — Run all setup scripts (sudo, torrent cron) non-interactively
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
- Quiet hours: 23:00–08:00 Asia/Bangkok (respect by agents and cleanup tasks).
