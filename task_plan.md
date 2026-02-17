# Workspace Builder Task Plan
**Date**: 2026-02-17 01:00 UTC
**Session**: cron:23dad379-21ad-4f7a-8c68-528f98203a33
**Goal**: Strategic workspace improvements aligned with long-term objectives

## Phases

### Phase 1: Context & Diagnostics
- [x] Read AGENTS.md, USER.md, recent daily logs
- [x] Check active-tasks.md, git status, recent commits
- [x] Search memory for relevant past decisions and findings
- [x] Run system health check (quick health)
- [x] Inspect gateway status and logs
- [ ] Verify cron job status (openclaw cron list)

### Phase 2: Identify Critical Issues
- [x] Gateway service failing (stale process, port conflict)
- [ ] MEMORY.md oversized (exceeds injection limit)
- [ ] __pycache__ directories accumulating (hygiene)
- [ ] System updates pending (31 packages)
- [ ] systemd linger not enabled (service orphan risk)

### Phase 3: Implement Improvements
- [ ] Fix gateway: stop stale process, restart clean
- [ ] Trim MEMORY.md to fit within limit (~6KB)
- [ ] Add cleanup script for __pycache__ directories
- [ ] Optionally apply pending system updates (documented, not forced)
- [ ] Document systemd linger as recommended manual action
- [ ] Archive previous builder artifacts to builds/ (if any)
- [ ] Update active-tasks.md with builder status

### Phase 4: Validation
- [ ] Run quick health → clean
- [ ] Verify gateway RPC reachable
- [ ] Test quick commands (mem search, verify)
- [ ] Check git status clean
- [ ] Ensure no temp files left
- [ ] Run quick verify

### Phase 5: Commit & Wrap
- [ ] Commit changes with prefix 'build:'
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark validated, add verification results
- [ ] Write summary to daily log (memory/2026-02-17.md)

---

## Notes
- Keep changes small but meaningful
- Follow close-the-loop protocol strictly
- If any step fails, debug before proceeding
