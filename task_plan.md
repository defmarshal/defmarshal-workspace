# Task Plan: Add Systemd Linger Validation

**Goal**
Enhance workspace validation to ensure systemd lingering is enabled for the ubuntu user, guaranteeing that openclaw-gateway and other user services persist across logout/reboot.

**Motivation**
- Lessons learned (MEMORY.md) identify systemd linger as required for reliable 24/7 operation.
- Current validation (`quick validate-constraints`) does not check this critical setting.
- Proactive detection prevents silent loss of agents after logout or reboot.

**Scope**
- Modify `scripts/validate-constraints.sh` to add a new constraint check for `/var/lib/systemd/linger/ubuntu`.
- Update the help text in `quick` (show-validation-checks command) to list this new check.
- Ensure the check passes on current system; treat missing linger as error.
- No other scripts or systems affected.

**Steps**
1. Update active-tasks.md: register this session as running.
2. Review existing validation logic and decide where to insert new check.
3. Implement the new check in `scripts/validate-constraints.sh`.
4. Update the `show-validation-checks` help text in `quick`.
5. Run `./quick validate-constraints` to verify all constraints pass (including new check).
6. If any failure: debug, adjust implementation, repeat step 5.
7. After passing, commit changes with prefix `build:` and push to origin/master.
8. Update active-tasks.md: mark this session as validated and add verification notes.
9. Append summary to daily log `memory/2026-03-02.md`.
10. Verify no temp files remain; confirm git clean.

**Success Criteria**
- `./quick validate-constraints` exits 0 and displays ✅ for systemd linger check.
- `quick show-validation-checks` includes the new item.
- Changes are committed and pushed; active-tasks.md updated correctly.
- All pre-existing constraints remain satisfied.

**Error Handling**
- If the linger file check fails (missing file), the constraint will fail. Investigate whether linger should be enabled; if it is unexpectedly missing, enable it via `sudo loginctl enable-linger ubuntu` as a remediation step.
- If script modification causes syntax errors, fix immediately and re-test.
