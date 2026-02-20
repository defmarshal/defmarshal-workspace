# Dev Cycle Plan — 2026-02-20 01:03 UTC

## Goal
Refactor `scripts/validate-cron-schedules.sh` to derive intended schedules from `CRON_JOBS.md` instead of hard-coded associative arrays. This prevents configuration drift and reduces maintenance overhead.

## Steps
1. Parse CRON_JOBS.md to extract job name, schedule expression, and timezone for each OpenClaw cron job.
2. Replace the INTENDED_EXPR and INTENDED_TZ arrays with dynamic parsing.
3. Keep the comparison and correction logic intact.
4. Test with `./quick cron-schedules` to ensure it still validates correctly.
5. Commit changes with `dev:` prefix.

## Success Criteria
- Validator script no longer contains hard-coded schedule expressions for each job.
- All cron jobs still validated correctly against documentation.
- Script remains simple and maintainable (bash-compatible).
- `./quick cron-schedules` exits with "All cron schedules match" when in sync.

## Notes
- CRON_JOBS.md format: job name in bold (`**job-name**`) followed by `- **Schedule**: ... (\`expr\`)` and optional `tz` mention.
- We'll extract using grep/sed/awk; no external dependencies beyond jq for cron JSON.
- Keep a fallback to current behavior if parsing fails (exit with error message).
