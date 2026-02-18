# Workspace Builder Findings

**Start time**: 2026-02-18 01:00 UTC

## Initial Assessment

System is healthy overall. Recent build (Feb 17) fixed meta-agent memory reindex logic. However, a critical bug remains in agent-manager.sh with identical inverted memory-reindex-check logic. This causes agent-manager to attempt reindex every 30 minutes when the system is clean, and skip when reindex is actually needed.

Additionally, the torrent-bot memory store shows dirty and failing reindex due to Voyage rate limits. This likely stems from the agent-manager bug triggering unnecessary reindex attempts.

## Issues Identified

### 1. Critical Bug: agent-manager.sh Inverted Logic

**Location**: `agents/agent-manager.sh`, lines ~43-46

**Current code**:
```bash
if ./quick memory-reindex-check >/dev/null 2>&1; then
  log "Memory reindex needed; triggering"
  ./quick memory-index >> "$LOGFILE" 2>&1 || true
fi
```

**Problem**: The condition triggers when `memory-reindex-check` exits 0 (OK). It should trigger when exit code is non-zero (needed or error). This is exactly the bug fixed in meta-agent two days ago.

**Impact**:
- Reindex attempted every 30min even when not needed (wastes API calls, hits rate limits)
- When reindex actually needed (dirty/stale), it's skipped
- Causes Voyage 429 errors, fills logs
- Torrent-bot store gets flagged dirty and repeatedly fails

**Fix**: Change to:
```bash
if ! ./quick memory-reindex-check >/dev/null 2>&1; then
  log "Memory reindex needed; triggering"
  ./quick memory-index >> "$LOGFILE" 2>&1 || true
fi
```
OR
```bash
./quick memory-reindex-check >/dev/null 2>&1
if [ $? -ne 0 ]; then
  log "Memory reindex needed; triggering"
  ./quick memory-index >> "$LOGFILE" 2>&1 || true
fi
```

### 2. Torrent-bot Memory Store Dirty & Failing

**Observation**:
- `quick memory-status` shows:
  - main: 15/15 files, 43 chunks, dirty: no
  - torrent-bot: 0/15 files, 0 chunks, dirty: yes
- `quick voyage-status` shows recent 429 errors for torrent-bot reindex

**Root cause**: agent-manager bug triggers unnecessary reindex attempts; Voyage rate limits cause failures; store remains dirty.

**Expected behavior**: Once agent-manager logic is fixed, unnecessary reindex attempts will stop. But we should also consider:
- Should torrent-bot store be reindexed at all? It's used by the torrent-bot daemon.
- Could we skip non-critical stores when Voyage is rate-limited?

### 3. Memory Observability Could Be Improved

- `quick memory-status` shows both stores but doesn't highlight dirty flag prominently
- No quick way to see which specific stores need attention
- Users may not realize there are separate memory stores (main vs agent-specific)

### 4. Voyage Rate Limit Handling Already Good

- Rate-lock mechanism (6h) in place after 429
- Meta-agent correctly disabled reindex
- Documentation in TOOLS.md is clear

## Proposed Solutions

- **Fix agent-manager.sh** with proper exit code check (mirror meta-agent fix)
- **Disable memory auto-reindex** for all stores until Voyage payment added (or use very conservative schedule)
- **Improve memory-status output** to show dirty status per store clearly
- **Add documentation** about memory stores and when to reindex
- **Test** agent-manager --once to verify correct behavior

## System Strengths

- Quick launcher well-developed with many utility commands
- Fallback grep search works reliably
- Health monitoring robust
- Cron scheduling solid
- Previous meta-agent fix demonstrates good pattern

## Risks

- Continuing to spam Voyage API could lead to longer-term blocking
- Stale memory index may degrade search quality over time (but fallback grep still works)
- Bug in agent-manager may have been causing unnecessary load for weeks

## Decision Log

- Will not enable auto-reindex for Voyage until payment added
- Will fix agent-manager logic as top priority
- Will keep memory-reindex as manual operation with clear check
- Will not separate stores at this time; just fix the trigger logic
