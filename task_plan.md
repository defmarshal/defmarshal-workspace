# Workspace Builder Plan

**Session ID:** 23dad379-21ad-4f7a-8c68-528f98203a33
**Triggered:** 2026-02-22 05:00 UTC
**Goal:** Implement meaningful workspace improvements while keeping changes small but valuable.

## Analysis

- **Git status:** Untracked research TTS .mp3 files (~200 files, some large) clutter working tree
- **Untracked script:** `scripts/tts-random.sh` exists but not committed nor integrated into quick launcher
- **Active tasks:** Contains archived/validated entry that should be removed to maintain <2KB limit
- **Overall health:** Disk 64%, updates none, memory clean, gateway healthy

## Objectives

1. Prevent git status noise from TTS output files by adding appropriate ignore patterns
2. Integrate the `tts-random` utility into the repo and quick launcher
3. Prune active-tasks.md of completed entries
4. Validate system health and commit changes
5. Follow close-the-loop protocol before marking complete

## Steps

- [ ] **Step 1:** Add `*.mp3` to `.gitignore` (global ignore for audio artifacts)
- [ ] **Step 2:** Commit `scripts/tts-random.sh` to repository (track the utility)
- [ ] **Step 3:** Add `tts-random` command to `quick` launcher script
- [ ] **Step 4:** Remove archived workspace-builder entry from `active-tasks.md`
- [ ] **Step 5:** Run verification: `quick health`, check git status, ensure no temp files
- [ ] **Step 6:** Commit all changes with prefix `build:`
- [ ] **Step 7:** Push to origin and verify
- [ ] **Step 8:** Update `active-tasks.md` with validation notes (if applicable)

## Validation Criteria

- `git status` shows only tracked changes (no untracked .mp3 files after ignore)
- `quick tts-random` works (quick command exists)
- `active-tasks.md` size < 2KB and contains only current/active entries
- System health passes (`quick health` shows all OK)
- Commits are pushed to GitHub

## Risks & Mitigations

- Risk: Adding `*.mp3` globally could hide legitimate audio files. Mitigation: No known mp3 assets should be tracked; research .mp3 are generated outputs.
- Risk: `quick` launcher syntax error. Mitigation: Test with `bash -n quick` and `./quick tts-random` before commit.
- Risk: Removing wrong entry from active-tasks. Mitigation: Only remove the entry that is already marked "validated" and archived in daily log.

## Notes

- Keep changes focused; avoid unrelated refactoring.
- Follow AGENTS.md guidelines: update active-tasks after spawn/kill; maintain size limits.
