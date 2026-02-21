# Task Plan: Workspace Builder - Strategic Improvements

**Date**: 2026-02-21
**Phase**: 1 (Planning)
**Agent**: workspace-builder

---

## Executive Summary

Perform comprehensive workspace health check and implement targeted improvements based on current state analysis. Focus areas: branch hygiene, documentation accuracy, system validation, and preventive maintenance.

---

## Phase 1: Assessment & Discovery (Status: pending)

### Step 1.1: Repository State Analysis
- Check current branch status and identify orphaned/unfinished branches
- Verify git status clean
- Review recent commit history for proper prefixes
- Inspect `.gitignore` completeness

**Success criteria**: Clear understanding of branch health and git state

### Step 1.2: Documentation Audit
- Validate CRON_JOBS.md for accuracy (detect duplicate numbering, outdated info)
- Review active-tasks.md size (<2KB) and format compliance
- Check AGENTS.md, TOOLS.md, HEARTBEAT.md for needed updates
- Verify all markdown files have proper formatting

**Success criteria**: Documentation gaps and errors identified

### Step 1.3: System Health Metrics
- Run comprehensive health check (`./quick health`)
- Check memory system status (provider, stores, dirty flag)
- Verify cron job health (`quick cron-health`)
- Check for orphaned agent sessions

**Success criteria**: Baseline health metrics recorded

### Step 1.4: Active Agents Review
- List running sessions/agents
- Verify agent-manager-cron status
- Check recent agent logs for errors
- Validate idea generator/executor status

**Success criteria**: All agents healthy or issues documented

---

## Phase 2: Implement Improvements (Status: pending)

Based on findings from Phase 1, implement:

### Step 2.1: Branch Management
- Clean up stale/unused branches (`git branch --merged`, manual review)
- Close abandoned work branches (like `idea/add-error-boundaries-to-the` if incomplete)
- Update active-tasks.md after any spawns/kills

**Validation**: `git branch` shows only relevant branches; active-tasks.md <2KB

### Step 2.2: Documentation Fixes
- Fix CRON_JOBS.md duplicate numbering (dev-agent-cron and content-agent-cron both labeled "8")
- Update any outdated cron schedules or descriptions
- Ensure all files have proper front-matter and current info
- Add any missing agent documentation

**Validation**: CRON_JOBS.md properly numbered; `quick help` reflects reality

### Step 2.3: System Optimizations
- If memory dirty, schedule gentle reindex (respect rate limits)
- Clean up any stale lock files or agent artifacts (with --execute if needed)
- Verify quiet hours are removed system-wide as documented
- Check disk usage and cleanup thresholds

**Validation**: `./quick health` passes; no alerts; memory clean

### Step 2.4: Validation & Testing
- Run `./quick validate` or comprehensive checks manually
- Test modified quick commands
- Verify cron schedule integrity with `quick cron-schedules`
- Check `active-tasks.md` format and size

**Validation**: All validation steps pass

---

## Phase 3: Finalization (Status: pending)

### Step 3.1: Commit Changes
- Stage all improvements
- Commit with prefix `build:` followed by descriptive message
- Push to origin
- Include today's workspace builder activity in daily memory

**Validation**: Commits pushed successfully; GitHub shows changes

### Step 3.2: Active Tasks Update
- Mark session as validated in active-tasks.md
- Add verification notes (commands tested, files modified)
- Ensure active-tasks.md remains <2KB

**Validation**: active-tasks.md updated and compact

### Step 3.3: Close the Loop
- Run final health check (`./quick health`)
- Verify no temp files left in workspace root
- Confirm git status clean
- Document outcomes in findings.md

**Success criteria**: System validated, clean, and documented

---

## Risk Mitigation

- **Before each destructive operation** (branch deletion, file cleanup): verify with dry-run flags first
- **Preserve branch `master` and `main`**; only delete clearly stale branches
- **Never commit secrets**: double-check `.gitignore` before any git adds
- **Respect rate limits**: memory reindex uses 120s spacing; don't run multiple heavy ops concurrently
- **Active tasks management**: update immediately after spawning/killing agents

---

## Notes

- This plan will be updated after each phase with actual results
- Findings and progress will be documented continuously
- If any step fails, debug before proceeding to next step
- The goal is small but meaningful improvements – not massive refactoring
