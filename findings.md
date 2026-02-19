# Findings: Cron Documentation Audit

**Date:** 2026-02-19 (fresh workspace-builder run)
**Session:** agent:main:cron:23dad379-21ad-4f7a-8c68-528f98203a33

---

## System Snapshot

- **Health:** ✓ All OK (Disk 42%, Gateway healthy, Memory clean, Git clean)
- **Cron Status:** 21 OpenClaw cron jobs, all running with correct schedules
- **Validation:** `./quick validate` passes

---

## Documentation Gap Identified

### Missing OpenClaw Cron Jobs

The following jobs are present in the system but absent from CRON_JOBS.md:

1. **notifier-cron**
   - Schedule: Every 2 hours (`0 */2 * * *`) in UTC
   - Description: Monitors cron failures, disk usage, gateway status; sends Telegram alerts
   - Log: `memory/notifier-agent.log`
   - Source: `agents/notifier-agent.sh`

2. **git-janitor-cron**
   - Schedule: Every 6 hours (`0 */6 * * *`) in UTC
   - Description: Git janitor cycle (maintenance, auto-commit thresholds)
   - Log: `memory/git-janitor.log`
   - Source: `agents/git-janitor-cycle.sh`

3. **archiver-manager-cron**
   - Schedule: Weekly Sunday at 02:00 UTC (`0 2 * * 0`)
   - Description: Archiver manager for content/research archives
   - Log: `memory/archiver-manager.log`
   - Source: `agents/archiver-manager.sh`

### System Cron Discrepancy

CRON_JOBS.md states: "gateway-watchdog runs every 5 min via system crontab". Actual system crontab shows:
```
0 * * * * /home/ubuntu/.openclaw/workspace/scripts/gateway-watchdog.sh
```
It runs **hourly**, not every 5 minutes (the 5-minute check is performed by `supervisor-cron` via OpenClaw). The System Cron section should be corrected.

### email-cleaner-cron

Not present in the current cron list. Likely deprecated. No action needed.

---

## Verification Plan

- Add missing job entries to CRON_JOBS.md with accurate schedules and descriptions
- Correct the gateway-watchdog description and schedule in the System Cron section
- Ensure formatting matches existing documentation style
- After update, re-read CRON_JOBS.md to confirm completeness and proper markdown

---

## Why This Matters

- Single source of truth: Accurate documentation prevents confusion during maintenance and onboarding
- Audit trail: Knowing all scheduled tasks helps with troubleshooting and capacity planning
- Compliance: Periodic synchronization ensures documentation doesn't drift from reality

---

## Conclusion

This is a straightforward documentation update with low risk and high clarity benefits. No functional changes required.
