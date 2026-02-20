# Workspace Builder Task Plan — Fresh Cycle
**Session:** cron:23dad379-21ad-4f7a-8c68-528f98203a33  
**Timestamp:** 2026-02-20 03:00 AM UTC  
**Goal:** Address outstanding opportunities and enhance system reliability

---

## Phase 1: Assessment & Planning

### Discoveries
- Git status: clean, up-to-date with origin
- Recent Agni cycle found TODOs but Rudra only modified scanner (didn't implement features)
- Outstanding TODO items:
  - `torrent-bot/main.py`: pause, resume, remove commands (marked TODO)
  - `skills/neural-memory/SKILL.md`: on-chain verification (lower priority)
- System health: all OK (Disk 42%, Gateway healthy, Memory clean)
- No active agents running

### Identified Improvements (Prioritized)
1. **Implement torrent-bot pause/resume/remove** — Complete the torrent management commands
2. **Review and optimize Agni opportunity handling** — Ensure Rudra actually addresses found items
3. **Update documentation** — Reflect new commands in README/help
4. **Validation** — Test new commands, run health checks, ensure no regressions
5. **Commit with `build:` prefix** — Follow convention

---

## Phase 2: Execution Steps

### Step 1: Analyze torrent-bot current state
- Read `torrent-bot/main.py` to understand existing command structure
- Identify how to implement pause/resume/remove using aria2 RPC
- Check existing command implementations (list, add, status) as templates

### Step 2: Implement missing torrent commands
- Add `torrent_pause(gid)`: call `aria2.tellStatus` then `aria2.pause`
- Add `torrent_resume(gid)`: call `aria2.unpause`
- Add `torrent_remove(gid)`: call `aria2.remove` (with file removal option)
- Add proper error handling and user feedback
- Update help text/command listing

### Step 3: Update documentation (if applicable)
- Update ANIME_COMPANION_README.md or any docs that describe torrent commands
- Add examples for new commands

### Step 4: Test implementation
- Dry-run: verify script syntax (`bash -n` doesn't work for Python, use `python -m py_compile`)
- Functional test: if aria2 is running, test each command with a safe gid (or simulate)
- Check that error messages are clear

### Step 5: Comprehensive validation
- Run `./quick health`
- Check `./quick torrent-status` (ensure it still works)
- Verify memory status
- Ensure no temp files, workspace clean
- active-tasks.md size < 2KB

### Step 6: Commit and push
- Stage changes: `git add -A`
- Commit message: `build: implement torrent-bot pause/resume/remove commands; enhance completeness`
- Push to origin
- Update active-tasks.md: mark this builder session as validated, then remove entry

---

## Phase 3: Close the Loop
- Re-run health check after push
- Optionally test Agni opportunity handling separately (out of scope for this build)
- Document final status in `progress.md`
- Ensure workspace builder self-clears from registry

---

## Risks & Mitigations
- **Breaking existing torrent commands** — Implement conservatively, test thoroughly
- **Aria2 RPC auth issues** — Use existing RPC secret handling pattern; don't hardcode credentials
- **Incomplete feature** — Ensure all three commands implement proper feedback to user

---

## Success Criteria
✅ Pause, resume, remove commands added and documented  
✅ Existing torrent functionality unaffected  
✅ All health checks pass  
✅ Changes committed with `build:` prefix and pushed  
✅ active-tasks.md remains under 2KB after cleanup  
