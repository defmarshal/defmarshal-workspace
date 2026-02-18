# Torrent Manager Agent

Unified daemon that combines:
- Keepalive of a persistent `torrent-bot` session (slash‑command interface)
- Automatic random torrent fetching from Nyaa (every 2 hours)

## Files

- `agents/torrent-manager/loop.sh` — main daemon loop
- `active-tasks.md` — entry: `[daemon] torrent-manager (running)`
- Cron job: `random-torrent-downloader` will be **removed** after migration

## Behavior

- Starts an `openclaw agents spawn` session with label `torrent-manager` if none exists
- On each cycle (2 h):
  - Quiet hours check (disabled by default; set `QUIET_HOURS=1` to enable UTC+7 23:00–08:00)
  - Disk space guard (skip if ≥90% full)
  - Run random picker: top 20 Nyaa, ≤1 GB, random pick, dedupe, `quick torrent-add`
- Logs to syslog with tag `torrent-manager`

## Migration Steps

1. Ensure new script is executable (`chmod +x agents/torrent-manager/loop.sh`)
2. Stop old daemon: `pkill -f agents/torrent-bot/loop.sh`
3. Start new daemon: `nohup agents/torrent-manager/loop.sh >> memory/torrent-manager.log 2>&1 &`
4. Remove cron: `openclaw cron remove random-torrent-downloader`
5. Update `active-tasks.md`: replace `[daemon] torrent-bot` with `[daemon] torrent-manager`
6. Verify: `./quick daemons` shows `torrent-manager` PID
7. Wait one cycle; check `memory/torrent-manager.log` and `aria2` for new additions

## Rollback

- Restart old daemon: `nohup agents/torrent-bot/loop.sh >> memory/torrent-bot.log 2>&1 &`
- Re‑add cron: `openclaw cron add ...` (from previous config)
- Update `active-tasks.md` back to `torrent-bot`
