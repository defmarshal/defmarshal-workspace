# Task Plan: Modernize dashboard and clean up deprecated memory/cron artifacts

## Goal
Update the workspace dashboard to use the new `openclaw memory search` command with JSON output instead of the deprecated `./msearch` script, and remove the obsolete `summarize-day` cron job to keep the workspace clean and aligned with the current memory system.

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [x] Review current dashboard implementation (uses `./msearch`)
- [x] Identify that `./msearch` is deprecated per MEMORY.md
- [x] Verify `openclaw memory search` works and supports `--json`
- [x] Check `summarize-day` cron job exists in crontab and script exists
- [x] Review active-tasks.md to avoid conflicts
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Decide to replace msearch with openclaw memory search (JSON parsing)
- [x] Plan to remove summarize-day cron entry (and optionally archive script)
- [x] Ensure dashboard output remains similar (file: snippet)
- **Status:** complete

### Phase 3: Implementation
- [ ] Modify dashboard.py's `search_memory` function to call `openclaw memory search --json` and parse results
- [ ] Test dashboard runs without errors and shows memory mentions
- [ ] Remove `summarize-day` entry from user crontab
- [ ] Optionally remove or comment `summarize-day` script (or leave as historical)
- **Status:** in_progress

### Phase 4: Testing & Verification
- [ ] Run `./dashboard.py` and verify memory section displays
- [ ] Run `quick health` to ensure system health is okay
- [ ] Check that no temporary files are left
- [ ] Verify git shows modifications to dashboard.py and CRON_JOBS.md (if changed)
- **Status:** pending

### Phase 5: Delivery
- [ ] Commit changes with prefix 'build:'
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark this workspace-builder session validated and add verification results
- [ ] Write summary for user
- **Status:** pending

## Key Questions
1. Does `openclaw memory search --json` provide sufficient data to replicate the old dashboard's "file: snippet" format? (Yes, JSON includes path, startLine, endLine, snippet)
2. Should we also update `quick mem` and `quick search` to use openclaw memory? (Defer; may interfere with dev-agent's work)
3. Is the `summarize-day` cron job definitely deprecated? (Yes, MEMORY.md notes it's deprecated; only cron uses it)

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use `openclaw memory search --json` in dashboard | Provides structured output, more robust than parsing grep lines; already available and working |
| Remove the `summarize-day` cron job | It's deprecated per MEMORY; only runs an unused script; reduces clutter |
| Do not modify `quick` memory commands in this build | Those files have uncommitted changes from dev-agent; avoid conflicts |

## Errors Encountered
(To be logged as they occur)

## Notes
- After implementation, ensure dashboard still displays "Recent memory mentions:" with up to 2 entries
- Update CRON_JOBS.md to reflect removal of Daily Memory Summarization job
- Commit should include modifications to dashboard.py and CRON_JOBS.md
- Verify that after commit, `git status` shows no remaining changes
