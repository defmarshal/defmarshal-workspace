# Task Plan: Add memory management commands to quick launcher

## Goal
Add `quick memory-status` and `quick memory-index` commands to simplify memory maintenance and monitoring, aligning with the long-term objective of a robust, searchable personal memory system.

## Current Phase
Phase 1: Requirements & Discovery

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand current memory CLI capabilities (openclaw memory status, index, search)
- [x] Determine useful additions to quick launcher
- [x] Decide on command names and behavior
- **Status:** in_progress

### Phase 2: Planning & Structure
- [ ] Document modifications to quick script
- [ ] Plan help text updates
- [ ] Plan testing steps
- **Status:** pending

### Phase 3: Implementation
- [ ] Edit quick: add cases for memory-status and memory-index
- [ ] Update help output
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Run `quick memory-status` and confirm output
- [ ] Run `quick memory-index` and confirm reindex
- [ ] Verify existing quick commands still work (mem, search, health)
- **Status:** pending

### Phase 5: Delivery
- [ ] Review changes (`git diff`)
- [ ] Commit with message "build: add memory-status and memory-index quick commands"
- [ ] Push to origin
- [ ] Update active-tasks.md with verification results
- [ ] Optionally update MEMORY.md with new tools
- **Status:** pending

## Key Questions
1. Should memory-index require confirmation? No, simple and safe.
2. Should memory-status output be raw or formatted? Default to raw status for now, can format later.
3. Should we add health check integration? Not in this build; keep scope small.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Add `memory-status` as pass-through to `openclaw memory status` | Provides quick access to index health without memorizing CLI |
| Add `memory-index` as pass-through to `openclaw memory index` | Allows user to manually reindex if needed |
| Keep output raw/unaltered | Simpler implementation, avoids parsing complexity |
| Do not modify existing commands | Avoid breaking changes |
| Do not integrate into `workspace-health` | Keep scope minimal; separate command is fine |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re-read this plan before major decisions
