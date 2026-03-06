# Cron Job Review & Redundancy Analysis
**Date**: 2026-03-06
**Status**: All jobs currently disabled (housekeeping mode)

## Summary

**Total OpenClaw cron jobs**: 28
- **Essential (keep)**: 8
- **Optional/experimental**: 11
- **Redundant/duplicate**: 4
- **Alerting/maintenance**: 5

**Recommendation**: Re-enable only **essential** jobs after housekeeping. Optional ones can be re-enabled later as needed.

---

## Essential Jobs (Core System & Production)

These are required for basic operation and daily value generation.

| Job | Purpose | Essential? | Notes |
|-----|---------|-----------|-------|
| `telegram-slash-handler` | Slash commands (/status, /health, etc.) | ✅ YES | Critical for CLI access via Telegram |
| `agent-manager-cron` | Prevents duplicate runs, cleans locks, monitors agent health | ✅ YES | System stabilizer; prevents chaos |
| `meta-supervisor-agent` | Keeps meta-supervisor daemon alive | ✅ YES | Meta-agent needs this daemon |
| `meta-agent-cron` | Autonomous planner; spawns sub-agents, commits improvements | ✅ YES | Core of self-extending system |
| `dev-agent-cron` | Builds utilities, fixes, improvements (dev: prefix) | ✅ YES | Active development cycle |
| `content-agent-cron` | Generates anime summaries, tech writeups, digests | ✅ YES | Content production |
| `research-agent-cron` | Conducts research, creates detailed reports | ✅ YES | Research pipeline |
| `git-janitor-cron` | Auto-commits, pushes, cleanup | ✅ YES | Git hygiene; prevents accumulation |

**Essential total**: 8 jobs

---

## Optional / Experimental Jobs

Nice-to-have but not critical. Can be disabled to save tokens/resources.

| Job | Purpose | Essential? | Notes |
|-----|---------|-----------|-------|
| `idea-generator-cron` | Generates 10 creative project ideas every 6h | ⚠️ Optional | Fun but not essential; high token use |
| `idea-executor-cron` | Executes one pending idea per cycle | ⚠️ Optional | Depends on idea-generator; can be manual |
| `evolver-agent-cron` | Proposes self-improvements (review mode) | ⚠️ Optional | Experimental; no auto-apply |
| `mewchat-evolver-cron` | Autonomous MewChat improvements | ⚠️ Optional | Specific to MewChat project |
| `game-enhancer-cron` | Game development enhancements | ⚠️ Optional | Niche; depends on game projects |
| `agni-cron` | Brainstorming + spawns Rudra executor | ⚠️ Optional | Creative ideation pipeline |
| `vishwakarma-cron` | Game planning + spawns Krishna builder | ⚠️ Optional | Game development specific |
| `youtube-digest-daily` | YouTube subscription digest | ⚠️ Optional | Personal preference; needs OAuth |
| `time-capsule-weekly` | Weekly time capsule archive | ⚠️ Optional | Curiosity/cool but non-essential |
| `daily-digest-cron` | Daily activity summary (currently disabled) | ⚠️ Optional | Can be manual; already disabled |
| `supervisor-cron` | Health monitoring (replaced by notifier) | ⚠️ Optional | Overlap with notifier; disabled |

**Optional total**: 11 jobs

---

## Redundant / Duplicate Jobs

These overlap with others and can be removed.

| Job | Duplicate Of | Why Redundant? | Recommendation |
|-----|--------------|----------------|----------------|
| `workspace-builder` | `dev-agent-cron` | Both implement workspace improvements; dev-agent is more active and focused. | ❌ Remove |
| `auto-torrent-cron` | `random-torrent-downloader` | Both add torrents; random-torrent-downloader already runs every 2h with disk checks. auto-torrent adds daily fixed batch. Choose one. | ❌ Remove (keep random-torrent-downloader) |
| `content-index-update-cron` | Covered by `agent-manager-cron` validation? | Content index updates are manual via `./quick content-index-update`. This cron is daily but may be unnecessary; can run on-demand. | ❌ Remove (manual when needed) |
| `log-rotate-cron` + `log-rotate-system-cron` | Two separate log rotation scripts | System cron already has daily log rotation. OpenClaw version is redundant. | ❌ Remove OpenClaw version (keep system) |

**Redundant total**: 4 jobs

---

## Maintenance & Cleanup Jobs

Automated cleanup; useful but can be manual if volume is low.

| Job | Purpose | Essential? |
|-----|---------|-----------|
| `cleanup-downloads-cron` | Deletes torrents older than 30 days | ⚠️ Useful but manual OK |
| `backup-cleanup-cron` | Keeps 1 backup tarball | ⚠️ Useful but manual OK |
| `cleanup-agent-artifacts-cron` | Removes stale lock files, empty plans | ⚠️ Useful but manual OK |
| `archiver-manager-cron` | Archives old content/research | ⚠️ Useful but manual OK |

**Maintenance total**: 4 jobs

---

## Alerting Jobs

| Job | Status | Notes |
|-----|--------|-------|
| `notifier-cron` | **Deleted** (2026-03-06) | Alerting disabled per user request |
| `supervisor-cron` | Disabled (inactive) | Overlap; not needed |

---

## System Cron (non-OpenClaw)

These are outside OpenClaw but workspace-related. Can be removed if OpenClaw gateway watchdog not needed.

| Entry | Purpose | Keep? |
|-------|---------|-------|
| `gateway-watchdog` | Restarts OpenClaw gateway if down | ⚠️ Optional if gateway stable; useful for reliability |
| `start-background-agents` (@reboot) | Launches agents on boot | ✅ Keep if using agents regularly |
| `aria2-slot-cleaner` | aria2 concurrency cleanup | ⚠️ Optional; monitor aria2 logs |
| `heartbeat-def` | Periodic heartbeat to Telegram | ⚠️ Optional; manual health checks OK |
| `rotate-logs` (system) | Compresses memory logs | ✅ Keep for log management |

---

## Final Recommendations

### After Housekeeping, Re-enable ONLY:

**Core System** (8 jobs):
1. telegram-slash-handler
2. agent-manager-cron
3. meta-supervisor-agent
4. meta-agent-cron
5. dev-agent-cron
6. content-agent-cron
7. research-agent-cron
8. git-janitor-cron

**Optional** (add back selectively as desired):
- daily-digest-cron (if you want daily summaries)
- youtube-digest-daily (if you use YouTube subscriptions)
- mewchat-evolver-cron (if actively developing MewChat)
- cleanup-downloads-cron, backup-cleanup-cron, cleanup-agent-artifacts-cron (maintenance)

**Remove permanently**:
- workspace-builder (duplicate)
- auto-torrent-cron (duplicate)
- content-index-update-cron (manual when needed)
- log-rotate-cron (system version sufficient)
- notifier-cron (already deleted)
- supervisor-cron (disabled)
- idea-generator-cron, idea-executor-cron, evolver-agent-cron, agni-cron, vishwakarma-cron, game-enhancer-cron, time-capsule-weekly (experimental/fluff)

**Reduces from 28 → 8–12 active jobs** (depending on optional selections), saving significant tokens and reducing noise.

---

## How to Prune

```bash
# Remove redundant jobs
openclaw cron remove <job-id>  # for each redundant job

# Disable optional jobs instead of removing
openclaw cron disable <job-id>
```

Keep the backup `cron-disable-backup-2026-03-06.md` for restoration if needed.

---

**Questions?** Let me know which optional jobs you want to keep, and I'll create a clean re-enable set.
