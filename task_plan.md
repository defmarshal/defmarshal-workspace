# Workspace Builder Task Plan

**Session ID:** workspace-builder-20260221-0100
**Start Time:** 2026-02-21 01:00 UTC
**Goal:** Diagnose meta-agent timeout, improve spawning logic, update documentation, and validate system

---

## Phase 1: Assessment & Diagnosis

**Status:** In Progress

### Tasks
1.1 Check meta-agent fix commit status (pushed? local?)  
1.2 Analyze meta-agent performance: run manually with `time` to measure duration  
1.3 Inspect meta-agent log to identify why it timed out on cron  
1.4 Check for overlapping runs or resource contention  
1.5 Document findings in `findings.md`

**Success Criteria:**
- Understand root cause of the 10-minute timeout
- Identify at least one concrete improvement to prevent recurrence
- All changes committed and pushed with `build:` prefix
- active-tasks.md updated and clean (<2KB)

---

## Phase 2: Implementation - Meta-Agent Improvements

**Status:** Pending

### Task 2.1: Add spawn debouncing / state tracking
- Create `memory/meta-agent-state.json` to track last spawn times for content-agent and research-agent
- Before spawning, check if we spawned that same agent type within the last 30 minutes
- If recent spawn exists, skip spawning and log "recent spawn, skipping"
- This prevents overlapping runs when agent hasn't produced output yet

### Task 2.2: Consider concurrent agent limit adjustment
- The `safe_to_spawn` already checks `SAFETY_MAX_CONCURRENT_AGENTS=10`. That's reasonable.
- Maybe add a specific check for meta-agent itself to avoid spawning when a previous meta-agent run is still active? Could cause the multiple runs seen in logs. But cron shouldn't start a new one if previous is still running. We'll skip for now unless diagnostics show overlapping.

### Task 2.3: Improve logging
- Add explicit timestamps and duration at start and completion (already have start; ensure completion logs always appear even on early exit? Use trap?)
- Use `log "Meta-Agent completed in ${duration}s"` at the end.

---

## Phase 3: Documentation & Validation

**Status:** Pending

- Update `MEMORY.md` with the meta-agent crash fix resolution and new debouncing improvement
- Update `active-tasks.md`: mark previous failed meta-agent entry as archived, add new builder entry
- Run `./quick health` to ensure system OK
- Validate: no temp files, no uncommitted changes except intended docs
- Commit all changes with proper `build:` messages
- Push to origin

---

## Notes
- The meta-agent fix (find instead of ls) is already in place (commit 9519b2e). Need to ensure it's pushed.
- The meta-agent-cron has a 600s timeout; typical runs should be <60s.
- The meta-supervisor daemon is running and monitoring; will report issues.
