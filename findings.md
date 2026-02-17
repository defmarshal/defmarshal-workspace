# Workspace Builder Findings
**Date**: 2026-02-17 (01:00 UTC run)
**Focus**: System health, critical service recovery, memory management, maintenance hygiene

## Current System State

### Disk & Storage
- Total: 45G, Used: 34.5G (77%), Free: 10.5G (healthy)
- Downloads: 10 files, 2.1G (all <30 days)
- Backups: 1 remaining backup tarball (2.2G) in /home/ubuntu (cleanup scheduled weekly)
- Agent logs: dev-agent.log (211K), content-agent.log (200K), research-agent.log (181K) — rotated weekly by log-rotate script

### Pending Updates
- 31 packages upgradable via apt (mix of security/bugfix)
- Updates-check and updates-apply scripts exist and are documented; applying is manual action

### Service Health
- **OpenClaw Gateway**: **CRITICAL** — systemd service repeatedly failing due to stale process holding port 18789.
  - Symptom: "Gateway failed to start: gateway already running (pid 97082); lock timeout after 5000ms"
  - Root cause: previous gateway instance not cleaned up; service enters restart loop (restart counter >100)
  - RPC probe: unreachable; cron jobs depending on gateway may fail or queue
- **Cron Jobs**: 13 OpenClaw cron jobs configured and documented in CRON_JOBS.md; last run status shows errors for workspace-builder due to gateway issues

### Memory System
- openclaw-memory: 7 files / 44 chunks (clean)
- Provider: Voyage AI with FTS (full-text search) enabled
- Index status: clean (dirty=no)
- Reindex scheduled weekly (Sunday 04:00 Asia/Bangkok)
- **Issue**: MEMORY.md oversized (15706 bytes, exceeds 6197 char injection limit). Causes truncation warnings during session bootstrap, potentially losing context.

### Code Hygiene
- No CRLF line endings in tracked files
- All shell scripts properly executable
- No large untracked files (>100 MB)
- **Issue**: Multiple __pycache__ directories present (not tracked, but clutter workspace). Could be cleaned periodically.

## Identified Improvements

### Critical (Fix Immediately)
1. **Gateway recovery** — Stop stale process, restart service cleanly. Must succeed for system functionality.
2. **MEMORY.md size reduction** — Split current oversized MEMORY.md into an index (MEMORY.md) and a historical narrative (MEMORY_HISTORY.md) to stay under injection limit and follow design principles.

### High Priority
3. **systemd linger** — Enable with `sudo loginctl enable-linger ubuntu` to keep gateway and user services alive across logout/reboot. Currently not enabled; on reboot, gateway may fail to start until manual intervention.
4. **Archive builder artifacts** — Create a `builds/` directory to archive planning files (task_plan.md, findings.md, progress.md) from each builder run after completion. Keeps workspace root clean while preserving audit trail.

### Medium Priority
5. **Pycache cleanup** — Add a script to clean __pycache__ directories, and optionally include in weekly hygiene (cron). Not urgent but improves tidiness.
6. **Updates mindfulness** — 31 packages pending. Could be applied manually with `quick updates-apply --dry-run` then `--execute` after review. Not automated due to risk; just monitor.

### Low Priority
7. **Cron failure alerting** — Currently logs per job but no central alert when cron jobs fail repeatedly. Could add a simple notification (out of scope for now).

## Recommendations & Action Plan

### Gateway Fix
- Run `gateway-fix.sh` which stops service, kills stray processes, and restarts fresh.
- Verify: `openclaw gateway probe` returns ok; `quick health` shows "Gateway: healthy".
- If still failing, check logs: `journalctl --user -u openclaw-gateway.service -n 50`.

### Memory Reorganization
- Rename current MEMORY.md to MEMORY_HISTORY.md (preserves full narrative).
- Create new concise MEMORY.md (~30 lines) containing only index/pointers:
  - Identity basics (name, timezone, assistant vibe)
  - High-level project list (link to projects.md)
  - Link to MEMORY_HISTORY.md for detailed timeline
  - Important resources and quick links
- Ensure size < 6KB to avoid truncation.
- Update AGENTS.md or any bootstrap that references MEMORY.md if needed (no changes likely; shorter is fine).

### Systemd Linger
- Manual action required (needs sudo):
  ```bash
  sudo loginctl enable-linger ubuntu
  loginctl show-user ubuntu -p Linger
  ```
- Document in MEMORY.md as a recommended one-time setup.
- Also ensure `start-background-agents.sh` handles gateway recovery if needed.

### Archive Build Artifacts
- Create directory `builds/` (if not exist).
- After each builder completion, move old task_plan.md, findings.md, progress.md into `builds/` with timestamped names (e.g., `build-2026-02-16-1900/`).
- For this run: after completion, clean up previous artifacts if any.

### Pycache Cleanup (Optional)
- Could add a script: `find . -type d -name __pycache__ -exec rm -rf {} +` (safe as they are caches)
- Add to quick launcher as `quick cleanup-pycache` or extend `hygiene` to also remove them (currently only reports).

## Risks & Mitigations

- **Gateway fix fails**: Might need deeper port conflict resolution. But pkill -9 should clear stale process.
- **Memory truncation**: If new MEMORY.md still too small to hold index, consider further trimming; essential info is already in other files.
- **Linger not enabled**: system reboot could stop gateway; documentation helps.
- **Updates application**: Applying 31 updates could cause breakage; always dry-run first. Not automated.

## Verification Checklist

- [ ] `quick health` passes (no CRITICAL, memory size reasonable, gateway healthy)
- [ ] `openclaw gateway probe` reachable
- [ ] `quick mem` and `quick search test` work (memory search functional)
- [ ] Git status clean; previous builder artifacts archived or committed
- [ ] No leftover temp files
- [ ] `quick verify` passes
- [ ] Changes committed with `build:` prefix and pushed
