# Task Plan: Workspace Audit & Targeted Improvements

## Goal
Perform a comprehensive workspace health audit and implement targeted improvements to maintain system reliability, complete pending maintenance tasks, and enhance documentation based on recent feature additions.

## Current Phase
Phase 1: Requirements & Discovery

## Phases

### Phase 1: Requirements & Discovery
- [x] Check active tasks and running agents
- [x] Retrieve neural-memory context (none found - new system)
- [x] Review MEMORY.md for recent changes and pending items
- [x] Run initial system health checks (disk, updates, memory status)
- [x] Verify git status and recent commits
- [x] Inspect cron jobs for duplicates/errors
- [x] Check memory system health (index dirty, torrent-bot empty)
- [ ] Document findings in findings.md
- **Status:** in_progress

### Phase 2: Planning & Structure
- [x] Define specific improvement tasks based on findings
- [x] Prioritize by impact and urgency
- [x] Create detailed implementation steps
- [x] Document decisions with rationale
- **Status:** complete

### Phase 3: Implementation
- [x] Fix memory system issues (reindex, clean dirty state)
- [x] Address system updates (apt upgrade)
- [x] Review and fix duplicate cron entries if needed
- [x] Update documentation (MEMORY.md, quick help, CRON_JOBS.md)
- [x] Add missing utilities if gaps identified
- [x] Validate agent health and logs
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Run `quick health` to verify system health
- [x] Test modified commands (memory-status, mem, search)
- [x] Verify memory indexing completes successfully
- [x] Check all files properly committed
- [x] Ensure no temp files left behind
- **Status:** complete

### Phase 5: Delivery
- [x] Review all output files
- [x] Ensure deliverables complete
- [x] Commit changes with prefix 'build:'
- [x] Push to GitHub
- [x] Update active-tasks.md with validation results
- **Status:** complete

## Key Questions
1. What is causing the memory system "dirty: yes" state and how should it be resolved?
   - Answer: Dirty flag indicates uncommitted changes. After index completes, should clear. Verify with `openclaw memory status` after index finishes. If persists, may need manual intervention or is normal after logging events.
2. Why does torrent-bot show 0 indexed files, and should it be indexed separately?
   - Answer: Each OpenClaw agent has its own memory store. Torrent-bot store is empty, which is expected if it hasn't logged anything yet. Should verify if it's needed - likely fine.
3. Are the duplicate cron entries for nyaa-top intentional or an error?
   - Answer: Duplicate identical lines in crontab is an error - likely accidental double-add. Should remove one to avoid duplicate downloads.
4. What documentation updates are needed to reflect the latest features (sudo, memory changes)?
   - Answer: MEMORY.md needs update to include sudo deployment and current memory system health status. CRON_JOBS.md already accurate but should note duplicate issue.
5. Should system updates (16 packages) be applied now or scheduled?
   - Answer: Apply now during builder window to maintain security and stability. Use elevated: true for apt operations.
6. Are there any broken symlinks, orphaned files, or temporary files to clean?
   - Answer: Check workspace for temp files, caches, etc. Should be minimal.
7. Does the quick launcher need additional commands or improvements based on recent usage?
   - Answer: Verify `memory-stats` exists (mentioned in MEMORY.md); if missing, add it.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Fix duplicate cron by removing one line | Avoid double downloads and wasted resources |
| Apply system upgrades via apt-get upgrade | Security/stability; 16 packages is significant |
| Use absolute path /home/ubuntu/.openclaw/workspace/quick for all testing | PATH inconsistency in exec context |
| Investigate memory dirty flag after index completes | Determine if it's a problem or normal state |
| Do NOT reindex torrent-bot memory yet | It's separate agent store; only reindex if needed later |
| Update MEMORY.md with current builder findings | Keep long-term memory current |
| Add verification checklist to active-tasks.md | Follow close-the-loop protocol |
| Commit changes with prefix 'build:' | Consistent with conventional commits |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| quick: command not found | 1 | Use absolute path in exec calls |
| sessions_list no output | 1 | Trust active-tasks.md and pgrep for agent status |

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re-read this plan before major decisions (attention manipulation)
- Log ALL errors - they help avoid repetition
- Respect quiet hours (23:00–08:00 UTC+7) - currently ~22:00 UTC+7, so proceed but be efficient
