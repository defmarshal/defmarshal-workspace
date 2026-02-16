# Workspace Builder Findings
**Date**: 2026-02-16 (21:00 UTC run)
**Focus**: Disk space analysis, backup strategy, and hygiene improvements

## Current Disk Status
- Filesystem: /dev/sda1 45G total, 36G used (82%), 8.2G free (⚠️ warning threshold)
- Workspace root: ~4.3G (downloads 2.1G, logs, scripts, skills, etc.)
- Home directory /home/ubuntu: 8.8G total (includes backups)

## Space Consumer Analysis

### Large Items in Workspace
- `downloads/` - 2.1G (torrent downloads, all from 2026-02-14, <30 days old)
- `aria2.log.2.gz` - 69M (rotated)
- `aria2.log.1.gz` - 13M (rotated)
- `.git/` - 77M (healthy)
- Agent logs: ~200K each, fine

**Observation**: Downloads are recent, so cleanup script won't delete yet; retention policy (30d) appropriate.

### Backup Tarballs (Primary Target)
- `/home/ubuntu/openclaw-backup-2026-02-16-1403.tar.gz` - 2.2G
- `/home/ubuntu/openclaw-backup-2026-02-16-1406.tar.gz` - 2.2G
- Created within 3 minutes of each other; likely redundant.
- Impact: 4.4G can be recovered by rotation/retention.

**Note**: Backup naming suggests manual or scripted process (`openclaw-backup-YYYY-MM-DD-HHMM.tar.gz`). No existing rotation scheme found.

## Existing Infrastructure
- `scripts/cleanup-downloads.sh` already implemented (dry-run, 30-day retention). Tested: no files older than 30 days.
- `cleanup-downloads-cron` exists (OpenClaw cron, weekly Sunday 06:00 Asia/Bangkok) – documented in cron list but not in CRON_JOBS.md yet.
- `quick health` already includes downloads metrics and disk thresholds (warning >=80%, critical >=90%).

## Identified Improvements

### High Priority
1. **Backup rotation/retention**: Implement cleanup script to prune old backups, keeping most recent N (default 1) to free space immediately.
2. **Document cleanup-downloads cron**: Update CRON_JOBS.md to reflect weekly cleanup-downloads job.
3. **Add `quick cleanup-backups`**: New launcher command for manual backup maintenance.

### Medium Priority
4. Consider scheduling weekly backup cleanup via cron to prevent recurrence.
5. Enable systemd linger for agent persistence across logout (requires user sudo action).

## Recommendations
- Create `scripts/cleanup-backups.sh` with safe defaults (--keep 1, dry-run)
- Integrate into `quick` launcher
- Document in CRON_JOBS.md (even if not scheduled yet)
- After implementation, run cleanup to recover ~2.2G (delete oldest of the two backups)
- Monitor disk trend; adjust retention if needed

## Risks & Mitigations
- Risk: Deleting all backups → Mitigation: script enforces --keep minimum, default 1; dry-run requires confirmation
- Risk: Accidentally deleting non-backup files → Mitigation: strict filename pattern `openclaw-backup-*.tar.gz` in /home/ubuntu only
- Risk: Cron misconfiguration → Mitigation: document carefully; use absolute paths

## Follow-up
- Verify `CRON_JOBS.md` completeness after updates
- Educate user on backup rotation and manual cleanup command
- Suggest manual `sudo loginctl enable-linger ubuntu` for agent reliability