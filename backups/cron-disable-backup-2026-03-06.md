# Housekeeping Backup - Cron & Agents State
**Created**: 2026-03-06 02:04 UTC
**Purpose**: Restore point before disabling all agents and cron

## OpenClaw Cron Jobs (24 total - all enabled before disable)

All jobs were enabled. Disabled via `openclaw cron disable <id>`.

Job IDs:
- e26c12bd-635a-48cf-bc8d-1707bc4ffd59 (telegram-slash-handler)
- 48a38fe2-9691-4bea-bed1-0f3313534fcd (dev-agent-cron)
- e345525c-f289-4eab-bf25-6d6fa065e4b0 (content-agent-cron)
- f69140f6-7341-4217-bad3-f4a9615b0b94 (research-agent-cron)
- 9112eca8-0ccb-4db4-b016-e5841fa9ef30 (idea-generator-cron)
- 4e9eb829-fcfd-4cb4-8139-44c299f7679a (game-enhancer-cron)
- 3291b8d1-cf95-4fed-8292-8dc724c38ae3 (meta-agent-cron)
- aadf040b-60d2-48ee-9825-0db68bb6c13b (random-torrent-downloader)
- 23788edb-575a-4593-a60e-7f94b9c95db6 (agni-cron)
- 86722825-c37c-4b96-a838-15cf224328e7 (idea-executor-cron)
- a27a9b33-e501-4ad2-97f5-2c02b05a743a (git-janitor-cron)
- 5d3597fc-6374-4cda-881a-0a1df677df87 (mewchat-evolver-cron)  # Note: ID typo in original? Actually: 5d3597fc-6376-4cda-881a-0a1df677df87
- 3cbadb80-f35c-4e4a-9c6e-0c14cc1c1974 (notifier-cron)  # DELETED 2026-03-06
- 6a1b4266-2a3d-4645-90a1-e07cde656b41 (evolver-agent-cron)
- 65f0d1f3-548c-4c4e-9215-241df8c67b95 (meta-supervisor-agent)
- 6e5621c3-783a-416c-93c7-56ea2cb4e920 (vishwakarma-cron)
- 16af6af1-b6e0-4435-91ba-15f7d04c0207 (daily-digest-cron)
- dada350a-4508-4358-8ac6-35f10e91cdd0 (content-index-update-cron)
- c6976c90-df08-4ac2-997a-a4a53be6c23c (youtube-digest-daily)
- b84b1f5c-7027-49f3-b9da-799721ecec21 (memory-reindex-cron)
- c6bca31f-9459-4cc7-a8dd-d35b268506e0 (log-rotate-cron)
- fb670b4f-717a-4a14-85e6-6ece389c8b61 (cleanup-downloads-cron)
- d5c6f526-52d7-4786-8dc0-4efff1f4e36b (backup-cleanup-cron)
- 6e4f5697-c2cc-48cb-91bb-0c4edcc19c46 (time-capsule-weekly)
- db19ad80-e15c-46d6-af15-8815366d638c (archiver-manager-cron)
- 6e07b8d1-c443-4a9f-a95e-665e47f29e52 (cleanup-agent-artifacts-cron)

## Deleted Permanently (2026-03-06)

- workspace-builder (23dad379-21ad-4f7a-8c68-528f98203a33) – redundant with dev-agent
- auto-torrent-cron (483e96ab-0837-4e5c-9086-a560635188af) – redundant with random-torrent-downloader
- notifier-cron (3cbadb80-f35c-4e4a-9c6e-0c14cc1c1974) – alerting disabled per user request
- idea-generator-cron (9112eca8-0ccb-4db4-b016-e5841fa9ef30) – low ROI, deleted 2026-03-06 06:20 UTC
- idea-executor-cron (86722825-c37c-4b96-a838-15cf224328e7) – low ROI, deleted 2026-03-06 06:20 UTC

## System Cron (user crontab) - OpenClaw-related entries

Original lines (before modification):
```
@reboot bash -c "sleep 60 && /home/ubuntu/.openclaw/workspace/start-background-agents.sh"
0 * * * * /home/ubuntu/.openclaw/workspace/scripts/gateway-watchdog.sh
*/5 * * * * /home/ubuntu/.openclaw/workspace/scripts/aria2-slot-cleaner.sh
0 */4 * * * /home/ubuntu/.openclaw/workspace/scripts/heartbeat-def.sh
0 2 * * * /home/ubuntu/.openclaw/workspace/scripts/rotate-logs.sh >> /home/ubuntu/.openclaw/workspace/memory/rotate-logs.log 2>&1
```

Modified: lines commented out with `#` prefix.

## Running Agents (active-tasks.md)

Before stop:
- meta-supervisor-daemon (PID: 856989) - Continuous auditor
- content-agent - last spawned 2026-03-06 02:04 UTC
- research-agent - last spawned 2026-03-06 02:04 UTC

All agents were terminated.

## Re-enance Instructions

To restore:
```bash
# Restore system crontab from backup
crontab /home/ubuntu/.openclaw/workspace/backups/crontab.bak

# Re-enable OpenClaw cron jobs (example for one job)
openclaw cron enable e26c12bd-635a-48cf-bc8d-1707bc4ffd59
# ...repeat for all job IDs above

# Restart meta-supervisor daemon
bash /home/ubuntu/.openclaw/workspace/agents/meta-supervisor/meta-supervisor-daemon.sh &
```

## Notes
- All OpenClaw cron jobs disabled at: 2026-03-06 02:05 UTC
- System cron entries commented at same time
- Agents killed via SIGTERM
- Backup of original crontab saved to: backups/crontab.bak
