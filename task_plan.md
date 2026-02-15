# Task Plan: Add Memory Display to Web Dashboard

## Goal
Add a memory section to the web dashboard (web-dashboard.py) that shows recent memories, making the memory system more accessible via the browser interface.

## Current Phase
Phase 1: Requirements & Discovery

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand current web dashboard structure
- [x] Identify that memory is missing from web dashboard (present in CLI dashboard)
- [x] Determine to add memory search results to /status endpoint and HTML UI
- [x] Check neural-memory context (empty - no past build memories)
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Design the memory data structure to return from /status
- [x] Plan HTML card addition and JavaScript integration
- [x] Decide on number of recent memories to show (e.g., 3)
- **Status:** complete

### Phase 3: Implementation
- [x] Modify web-dashboard.py: add function to fetch recent memories via `openclaw memory search`
- [x] Integrate into collect_status() with key "memory"
- [x] Update HTML: add a new card for recent memories
- [x] Update JavaScript refresh() to populate memory card
- [x] Test locally with `quick web`
- **Status:** complete

### Phase 4: Testing & Verification
- [ ] Verify web dashboard loads and displays memory card
- [ ] Verify memory entries appear with snippet and file
- [ ] Run `quick health` to ensure system health
- [ ] Check for any console errors in browser
- **Status:** in_progress

### Phase 5: Delivery
- [ ] Review all changes (web-dashboard.py)
- [ ] Commit with prefix 'build:'
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark session validated, add verification notes
- **Status:** pending

## Key Questions
1. How many recent memories should be displayed? (Decision: 3, similar to commits)
2. Should we show just the snippet and source file? (Yes, keep simple)
3. Should we include a search box? (No, out of scope for this small improvement; future enhancement)

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use `openclaw memory search "recent"` | Consistent with CLI dashboard behavior |
| Show 3 items | Keeps UI uncluttered, matches recent commits count |
| Display file name and first line of snippet | Simple, informative, fits card layout |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| neural-memory context empty | 1 | Proceed using MEMORY.md and existing knowledge; note in findings |

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re-read this plan before major decisions
