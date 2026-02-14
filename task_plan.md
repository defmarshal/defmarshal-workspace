# Task Plan: Enhance quick launcher usability

## Goal
Improve the `quick` command's output for memory commands to be human-friendly in interactive use while preserving machine-readable JSON when piped. Also clean up duplicate help text.

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [x] Read current `quick` script implementation
- [x] Identify issues: `mem` and `search` output raw JSON (not user-friendly for terminal)
- [x] Identify minor help text duplication (`nyaa-top` appears twice)
- [x] Determine desired behavior:
  - When stdout is a TTY, format output as "file: snippet" (like dashboard)
  - When piped or with `--json` flag, output raw JSON
  - For `search`, support optional `--json` flag and preserve it across limited results
- [x] Check for dependencies: Python3 is available; we'll use a small Python one-liner for formatting.
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Plan modifications to `quick` script:
  - Replace `mem` and `search` case blocks with conditional formatting
  - Detect TTY using `[ -t 1 ]`
  - Add `--json` flag handling for `search` (and maybe `mem` for consistency)
  - Ensure empty results handled gracefully
  - Fix help text: remove duplicate `nyaa-top` entry
- [x] Plan testing:
  - `quick mem` in terminal should show formatted lines
  - `quick mem | cat` should show raw JSON
  - `quick search "test"` formatted; `quick search "test" --json` raw JSON
  - `quick help` should not show duplicates
- [x] Commit changes with prefix 'build: quick mem/search formatting; help cleanup'
- **Status:** complete

### Phase 3: Implementation
- [ ] Modify `quick` script accordingly (edit)
- [ ] Test locally as described
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Run `quick mem` and verify output format
- [ ] Run `quick mem | wc -l` to ensure still produces output (JSON)
- [ ] Run `quick search "memory"` and verify formatting
- [ ] Run `quick search "memory" --json` to get raw JSON
- [ ] Run `quick help` and verify no duplicate lines
- [ ] Run `quick health` to ensure system health OK
- [ ] Check for temporary files (none expected)
- **Status:** pending

### Phase 5: Delivery
- [ ] Commit changes to `quick` with message 'build: quick mem/search human-friendly output; add --json; fix help dupes'
- [ ] Push to GitHub
- [ ] Update active-tasks.md: mark this workspace-builder session as validated and add verification results
- [ ] Remove session entry from active-tasks.md after validation (per AGENTS.md)
- [ ] Write summary for user
- **Status:** pending

## Key Questions
1. Should we also apply formatting to `quick mem` when output is piped? No, preserve raw JSON for pipelines.
2. Should we limit `mem` formatting to 20 results as before? Yes, same limit.
3. How to handle errors from openclaw memory command? Let errors propagate as before.

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use Python one-liner for formatting | No new dependencies, Python available; simple to implement inline |
| Add `--json` flag to `quick search` to preserve raw output | Maintains scriptability; default interactive TTY gets formatted |
| Do not modify `openclaw` invocation path | Already using absolute path; reliable |
| Fix help duplication by removing one `nyaa-top` block | Improves clarity of help output |

## Errors Encountered
(To be logged as they occur)

## Notes
- We'll use a small Python snippet to format JSON output. It will be embedded in the script, which may be messy but keeps changes minimal.
- We'll ensure the Python code gracefully handles missing results.
