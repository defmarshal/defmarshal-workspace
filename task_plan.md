# Task Plan: Clean memory docs, improve git hygiene, add agents command

## Goal
Clean up memory documentation, improve git hygiene by ignoring transient files, and add a more capable agents management command to the quick launcher.

## Current Phase
Phase 1: Assessment & Discovery

## Phases

### Phase 1: Assessment & Discovery
- [x] Check current memory documentation structure (memory/ dir, MEMORY.md)
- [x] Check git status and .gitignore coverage
- [x] Check current `quick agents` functionality
- **Status:** complete

### Phase 2: Clean Memory Docs
- [x] Remove MEMORY.md.bak (backup file)
- [x] Review memory/ directory: keep only necessary logs (clean old cron logs if any)
- [x] Ensure daily log files are following retention policy (keep recent, archive old if needed)
- **Status:** complete

### Phase 3: Improve Git Hygiene
- [x] Untrack dev-agent.log and memory/workspace-builder.log (git rm --cached)
- [x] Verify .gitignore covers cron logs (memory/*.log) and root logs (*.log) — already present
- [x] Add important untracked files: dev-agent-loop.sh, research/, skills/aria2/
- [x] Ensure build artifacts ignored (already covered)
- **Status:** complete

### Phase 4: Enhance Agents Command
- [x] Modify agents case to pass through flags to `openclaw sessions`
- [x] Preserve auto-JSON when piped (behavior unchanged)
- [x] Update help text to indicate flags are accepted
- **Status:** complete

### Phase 5: Testing & Verification
- [x] Test quick agents and quick agents --json (both produce correct output)
- [x] Run quick health (Disk 70%, Updates 15, Git dirty → will commit)
- [x] Test quick search "test" (returns results from memory)
- [x] Verify git status staged changes match intentions (no unwanted logs)
- **Status:** complete

### Phase 6: Delivery
- [x] Commit all changes with prefix 'build:'
- [x] Push to GitHub
- [x] Update active-tasks.md with verification results
- [x] Close the loop
- **Status:** complete

## Key Questions
1. Should we keep all memory daily logs indefinitely, or rotate/archive old ones? (Keep for now, but remove cron logs after 7 days)
2. Which agent logs should be ignored? All *.log files are already ignored, but some appear modified; need to ensure they are not staged.
3. What enhancements to agents command are most useful? At minimum: better formatting and JSON output.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use existing quick script for agents enhancements | Maintains unified interface, no new files |
| Keep all memory daily logs for now | Historical data may be valuable; can prune later |
| Add --json flag to agents for machine readability | Enables scripting and integration |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re-read this plan before major decisions
- Log ALL errors