# Task Plan: Enhance memory system monitoring in health/dashboard

## Goal
Integrate openclaw-memory health metrics into workspace-health and CLI dashboard for comprehensive system monitoring.

## Current Phase
Phase 1

## Phases

### Phase 1: Assessment & Planning
- [x] Review current memory system setup and monitoring tools
- [x] Identify gaps: workspace-health lacks memory metrics; CLI dashboard lacks stats
- **Status:** complete

### Phase 2: Enhance workspace-health with memory metrics
- [ ] Modify workspace-health script to include memory status (files, chunks, dirty, provider)
- [ ] Test: quick health should now include memory info (or run workspace-health directly)
- **Status:** pending

### Phase 3: Enhance CLI dashboard with memory stats
- [ ] Update dashboard.py to display memory system stats (matching web dashboard)
- [ ] Keep recent memory search as is, add a stats line above it
- **Status:** pending

### Phase 4: Validation & Testing
- [ ] Run `quick health` and verify memory metrics appear
- [ ] Run `quick dash` and verify memory stats are shown
- [ ] Run `quick memory-status` as fallback check
- [ ] Ensure no errors
- **Status:** pending

### Phase 5: Documentation & Delivery
- [ ] Update quick launcher help if needed
- [ ] Update MEMORY.md with new monitoring capabilities
- [ ] Commit changes with 'build:' prefix and push
- [ ] Update active-tasks.md
- **Status:** pending

## Key Questions
1. How to fetch memory status reliably in shell/Python? Use `openclaw memory status --json`.
2. Should we include FTS/vector/batch status? Yes, but keep summary concise (files/chunks/dirty/provider).
3. Format: one-line summary for workspace-health; multi-line for dashboard.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Add memory stats to workspace-health | Consolidated health view; already used for alerts |
| Add memory stats to CLI dashboard | Parity with web dashboard; better UX |
| Use openclaw memory status JSON output | Reliable, structured data |
| Keep output concise | Health needs one-line; dashboard can show a stats line |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re-read this plan before major decisions
- Log ALL errors
