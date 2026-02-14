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
- [ ] Remove MEMORY.md.bak (backup file)
- [ ] Review memory/ directory: keep only necessary logs (clean old cron logs if any)
- [ ] Ensure daily log files are following retention policy (keep recent, archive old if needed)
- **Status:** pending

### Phase 3: Improve Git Hygiene
- [ ] Update .gitignore to cover all transient files (aria2.session, specific agent logs, state files)
- [ ] Ensure build artifacts are ignored (__pycache__, .cache)
- [ ] Verify that important files are tracked (quick, scripts, documentation)
- [ ] Optionally commit cleanup changes (but not the final build yet)
- **Status:** pending

### Phase 4: Enhance Agents Command
- [ ] Extend `quick agents` with more filtering options (--json, --running, --daemon)
- [ ] Add support for agent actions (e.g., list, info, kill) if feasible
- [ ] Update help text accordingly
- **Status:** pending

### Phase 5: Testing & Verification
- [ ] Test quick agents new functionality
- [ ] Run quick health to ensure system health
- [ ] Test memory search (quick search test)
- [ ] Verify git status is clean (only intentional files)
- **Status:** pending

### Phase 6: Delivery
- [ ] Commit all changes with prefix 'build:'
- [ ] Push to GitHub
- [ ] Update active-tasks.md with verification results
- [ ] Close the loop
- **Status:** pending

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