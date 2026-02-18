# Workspace Builder Task Plan

**Started**: 2026-02-18 05:00 UTC
**Goal**: Prune active-tasks.md to enforce ≤2KB size limit by archiving completed build entries to daily memory log; verify system health; commit changes.
**Context**: Active-tasks.md currently ~4KB (41 lines) due to accumulated validated build entries from today (01:00 and 03:00). AGENTS.md policy states max 2KB. Need to maintain lean file for fast loading and token efficiency.

## Current State Analysis

- active-tasks.md size: 4.0K, 41 lines
- Contains:
  - Running daemon: torrent-bot
  - Validated builds: 2 entries (today's builds)
  - Completed (Feb 17) historical section (hand-rolled archive)
- System health: OK (disk 81%, gateway healthy, memory main clean)
- Memory stores: main clean; torrent-bot & cron-supervisor dirty (benign, documented)
- Recent commits: HEAD at 6ea3ede (content digest)
- No uncommitted changes

## Identified Issues & Opportunities

1. **active-tasks.md exceeds 2KB limit** — violates policy, increases token usage, slower reads.
2. **Completed build entries are retained** — should be archived to daily memory log and removed from active-tasks to keep only truly active tasks.
3. **Historical "Completed (Feb 17)" section** — could be moved to separate archive, but can keep short; focus on pruning current validated entries.
4. **Opportunity**: Enforce archival process as part of build validation routine.

## Task Phases

### Phase 1: Evaluate active-tasks.md Structure
- Parse current entries and classify by status (running vs validated vs old archive)
- Identify which entries to archive (validated builds from today)
- Ensure running daemon remains

**Status**: Not started

### Phase 2: Archive to Daily Memory Log
- Read memory/2026-02-18.md
- Append archival entries for the two validated builds with proper timestamps and verification summaries
- Preserve system context and commit references
- Append to daily log, maintaining format

**Status**: Not started

### Phase 3: Prune active-tasks.md
- Remove the two archived build entries from active-tasks.md
- Optionally shorten "Completed (Feb 17)" to a single line or remove (if moved elsewhere)
- Ensure file remains well-formed and under 2KB
- Keep running daemon entry and any other active agents

**Status**: Not started

### Phase 4: Add New Build Entry (self)
- Add entry for this build with key: [build] (or similar), goal, start time, status: running initially
- Will update to validated after verification

**Status**: Not started

### Phase 5: Validation & Testing
- Run `quick health` — should be OK
- Check active-tasks.md size — should be ≤2KB
- Verify that memory log updated correctly
- Ensure no other side effects
- Prepare commit message

**Status**: Not started

### Phase 6: Commit, Push, and Archive
- Commit changes with prefix 'build:' including:
  - active-tasks.md (pruned)
  - memory/2026-02-18.md (archival additions)
- Push to GitHub
- Update active-tasks.md entry to status: validated with verification notes
- Final validation

**Status**: Not started

## Success Criteria

- active-tasks.md size ≤ 2KB (ideally <1.5KB)
- Completed build entries removed and safely archived in memory/2026-02-18.md
- Running daemon entry preserved
- System health remains OK
- Changes committed and pushed
- active-tasks.md updated with this build's validation

## References

- Policy: AGENTS.md "Active Tasks Registry" section (max 2KB)
- Example archival: Completed (Feb 17) section in active-tasks.md
- Daily log structure: memory/2026-02-18.md
- Build workflow: planning-with-files skill
