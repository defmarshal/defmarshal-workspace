# Workspace Builder Task Plan

**Started**: 2026-02-18 01:00 UTC
**Goal**: Fix critical bug in agent-manager memory reindex logic; address torrent-bot memory store issues; improve system robustness
**Context**: Previous build (Feb 17) fixed meta-agent memory reindex logic; Voyage AI rate limits still active; system healthy but agent-manager has opposite bug causing unnecessary reindex attempts

## Current State Analysis

- Git status: clean, up-to-date
- System health: OK (disk 79%, 22 updates, gateway healthy)
- Memory: main store clean (15/15 files, 43 chunks), torrent-bot store dirty (0/15 files) and failing reindex due to Voyage 429
- Meta-agent: memory reindex correctly disabled; uses exit codes properly
- Agent-manager: has inverted memory-reindex-check logic (triggers reindex on exit 0, skips on exit 1)
- Voyage AI: rate limited on free tier (3 RPM); main store clean but torrent-bot reindex attempts fail

## Identified Issues & Opportunities

1. **CRITICAL BUG**: agent-manager.sh memory reindex check logic inverted
   - Currently: `if ./quick memory-reindex-check >/dev/null 2>&1; then` triggers reindex on success (exit 0)
   - Should be: trigger reindex when check returns exit 1 (reindex needed) or 2 (error)
   - Impact: agent-manager attempts reindex every 30 minutes even when not needed, causing Voyage rate limit hits and wasted cycles
   - Also: when reindex actually needed (dirty/stale), it skips

2. **Torrent-bot memory store dirty**
   - The torrent-bot agent has a separate memory store that shows dirty: yes
   - Reindex attempts for torrent-bot fail due to Voyage rate limits
   - Should either skip reindex for torrent-bot (like main) or ensure proper backoff

3. **Observability**: No clear per-store memory status
   - `quick memory-status` shows both stores but doesn't indicate which are dirty
   - Could add a quick command to check all stores individually

4. **Rate limit handling**: Need to ensure all reindex attempts respect Voyage limits and rate-lock

## Task Phases

### Phase 1: Fix agent-manager.sh Memory Reindex Logic
- Change logic to check for non-zero exit code (needed) instead of zero (ok)
- Add proper condition: `if [ $? -ne 0 ]; then` or `if ! ./quick memory-reindex-check; then`
- Test with dry-run to verify correct behavior
- Update comments to reflect correct exit code semantics

**Status:** Not started

### Phase 2: Handle Torrent-bot Store Reindex
- Option A: Disable reindex for torrent-bot store (similar to meta-agent) since Voyage is rate-limited
- Option B: Ensure memory-reindex-check and memory-index skip non-critical stores
- Investigate why torrent-bot store is dirty; determine if it actually needs reindex
- Add a way to selectively reindex only main store

**Status:** Not started

### Phase 3: Improve Memory Observability
- Enhance `quick memory-status` to clearly show dirty status per store
- Add `quick memory-dirty` to quickly list which stores need reindex
- Document store types and their purposes (main vs torrent-bot)

**Status:** Not started

### Phase 4: Testing & Validation
- Run agent-manager --once manually to verify correct reindex decision
- Check logs for proper behavior
- Test memory-status commands
- Ensure no unintended side effects

**Status:** Not started

### Phase 5: Documentation & Commit
- Update TOOLS.md with memory store details and management commands
- Update MEMORY.md if needed with current state
- Commit changes with prefix 'build:'
- Update active-tasks.md with verification results
- Push to GitHub

**Status:** Not started

## Success Criteria

- agent-manager.sh memory reindex logic fixed (triggers only when needed)
- Torrent-bot store either clean or reindex properly disabled/backoff
- `quick memory-status` clearly shows dirty flag per store
- System runs without unnecessary reindex attempts
- All changes tested, committed, and pushed
- active-tasks.md updated with validation notes

## References

- Previous build: 5cbd769, 9e4ac09
- Bug: agent-manager.sh line 43 (inverted condition)
- Voyage rate limit: 3 RPM free tier; payment required for higher limits
- Memory stores: main (active), torrent-bot (daemon store)
- Logs: memory/agent-manager.log, memory/memory-reindex.log
