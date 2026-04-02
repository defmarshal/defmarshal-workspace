# Lessons Learned

Recurring patterns, mistakes, and best practices. Load on demand via `memory_search` or direct read when context requires.

## OpenRouter API Issues

- **NoneType strip errors in code-gardener** → Error: `'NoneType' object has no attribute 'strip'` when processing OpenRouter responses. Happens when API returns None or malformed JSON. The code-gardener catches the exception and continues, but generated apps may have missing/incomplete content. Need to add response validation before accessing `.strip()`.
- **Empty content from OpenRouter** → Some responses return `null` or missing content fields. The code-gardener writes apps anyway, resulting in likely-empty or placeholder apps. Should add explicit check for non-empty content and retry logic with exponential backoff.

## Memory & Context

- **Voyage rate limits** (3 RPM) → fallback to grep-based search (`./msearch`) for reliability
- **OpenRouter credit exhaustion** → monitor usage; switch to free models when needed; have fallback providers
- **Summarization overhead** → daily cron at 22:30 Asia/Bangkok to batch process; avoids runtime token burn
- **Mental notes are lost** → always write to files. Session restarts clear context. Text > Brain.
- **Context bloat** → Use memory hierarchy (active-tasks.md → daily logs → thematic files → MEMORY.md index). Don't load everything.

## Agent Management

- **Orphaned agents** → Always record session keys in `active-tasks.md` when spawning. Track running state.
- **Sub-agent validation** → Close the loop: sub-agent self-validates AND you verify manually (curl, test commands). Never trust "all green" blindly.
- **Parallel isolation** → Independent tasks should run in separate agent instances with zero shared state. Avoids coordination overhead and race conditions.
- **Model selection** → Use cheaper models for internal tasks; reserve stronger models for web-facing work (avoid prompt injection from hostile content).
- **Quiet hours respect** → Previously 23:00–08:00 UTC+7, but **quiet hours removed system-wide** on 2026‑02‑17; all agents now run 24/7. Still check HEARTBEAT.md for current policy.
- **Persistent agent anti-pattern** → Do NOT use long-running subagents for periodic tasks. Use **cron jobs** instead. Gateway restarts kill subagents; cron auto-spawns fresh per run. Workspace-builder already converted to cron (Feb 13) — do the same for content-agent, research-agent, dev-agent.
- **Gateway restart behavior** → meta.lastTouchedAt changes cause full restart (Issue #11744). Config edits may kill subagents. Minimize config churn.
- **Systemd linger required** → Enable with `sudo loginctl enable-linger $USER` so user services survive logout/reboot. Without it, openclaw-gateway.service stops, killing all agents.
- **Session metadata survives, process does not** → sessions.json keeps conversation history, but the actual agent process dies on gateway exit. No auto-respawn. You must manually respawn or use cron.
- **Supervision options** — For truly persistent agents: (1) cron-based periodic fresh spawns (recommended), (2) separate systemd units with Restart=always, or (3) watchdog cron that checks `sessions list` and respawns missing agents.
- **Meta-Agent schedule corruption** → The resource-based scheduling adjustment (meta-agent) was flawed and caused unintended frequency changes (e.g., supervisor from 5min to hourly). **Disabled** on 2026‑02‑18. Cron schedules now strictly follow CRON_JOBS.md. A safety net (agent-manager validation) enforces integrity automatically.
- **Cron job frequency & rate limits** → Avoid extremely frequent cron intervals (e.g., every 15 minutes) for jobs that rely on rate-limited LLM APIs (OpenRouter free tier). Such jobs will fail with cooldown errors and trigger supervisor alerts. Adjust schedules to longer intervals (e.g., every 6 hours) or switch to non-LLM execution (system cron, systemEvent payload). Example: git-janitor-cron originally every 15 min → changed to every 6 hours on 2026‑02‑19 after repeated OpenRouter cooldowns.
- **Cron job state drift** → Documented inactive jobs (in CRON_JOBS.md) can become re-enabled accidentally (manual action, script error). This leads to unnecessary token consumption. Periodically run `openclaw cron list` and verify that jobs marked as "Inactive" in documentation are actually disabled. If drift detected, use `openclaw cron disable <id>` to restore intended state. Consider adding automated state validation to agent-manager to enforce documentation as source of truth.
- **Stale `runningAtMs` blocking execution** → Cron job may become stuck in "running" state if the agent exits without clearing it (e.g., early failure, signal kill). This blocks future runs. Recovery: manually clear `runningAtMs` via `cron update` (set to 0) or restart gateway. Add monitoring: if `nextRunAtMs` is in the past but `runningAtMs` is set, alert and auto-clear after timeout. Ensure agents always clear state on exit (trap EXIT).

## Git & Deployment

- **Embedded credentials** → Use HTTPS + PAT with `~/.git-credentials` and `git config --global credential.helper store`. Never commit tokens.
- **Commit hygiene** → Use prefix `build:` for workspace-builder commits. Clear purpose, easy to filter.
- **Push verification** → After push, confirm remote URL is correct (`git remote -v`) and no credentials leaked.

## Skill Installation

- **Bloat avoidance** → Install only skills with clear ROI. Remove unused ones. Check for conflicts before adding.
- **MCP servers** → After adding to `mcp.json`, restart gateway. Verify with `nmem_stats` or equivalent.
- **Skill updates** → Periodic `clawhub update --all` to keep skills current. Check changelogs for breaking changes.

## Tool Usage

- **TTS narration** → Edge TTS is free, no API key needed. Good for audio summaries.
- **Email cleaner** → Always dry-run first (`--max 1`). Review rules before `--execute`.
- **Memory search** → Use semantic search (`claw memory search`) over vector-based if rate limited. Simple grep as fallback.
- **Exit code vs output** → When writing conditional logic based on a script's result, use the command's exit code (`$?`) rather than parsing its stdout. Output is for human consumption; exit codes are for machine decisions. Prevents bugs like meta-agent always triggering due to multi-line status text.
- **OpenClaw CLI JSON parsing** → `openclaw ... --json` may prepend Doctor warnings (config notices) to stdout. Always filter with `sed -n '/^{/,$p'` before piping to `jq`. Example: `openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p' | jq ...`
- **Binary file detection in grep** → When scanning files for text patterns (like CRLF), use `grep -I` to ignore binary files. Binary files contain arbitrary bytes that can match any pattern and cause false positives.
- **jq output semantics** → The comma operator (`,`) in jq creates a stream of multiple outputs, not a single modified object. To chain modifications and emit a single JSON object, use the pipe operator (`|`). Example: `.status = $status | .implemented_at = $ts | .result = $result`. Using commas will write multiple JSON objects to the output, corrupting files expecting a single object. This bug caused enhancement-bot proposal corruption and temp file accumulation.

## Performance

- **Heartbeat efficiency** → Keep HEARTBEAT.md under 20 lines. Avoid burning tokens on trivial checks.
- **Cron batching** → Combine similar checks (email + calendar + weather) into single heartbeat to reduce API calls.
- **Parallel execution** → If tasks are independent, spawn all at once. Went from 45min to 8min on batch deployments through parallelization.

## Token Optimization

- **Aggressive max-tokens limits** → Using `--max-tokens` on agents can truncate output mid‑sentence or cause incomplete summaries, breaking downstream processing. Prefer prompt‑based soft constraints ("keep it brief") over hard caps until thoroughly tested. If caps are necessary, introduce incrementally and validate output quality before global rollout.
- **Conciseness directives in prompts** → Adding "Be extremely concise" can sometimes over‑constrain the model and lead to terse or incomplete outputs. Test with a few examples first to gauge effect. Monitor for regressions after changes.
- **Self‑correction via revert** → The system automatically reverted token optimization changes when output broke. This is a healthy safety mechanism. When a revert occurs, investigate the root cause before attempting re‑implementation.

## Script Hygiene

- **Define all variables** → When using `set -u`, ensure all variables are initialized before use. The `validate-cron-schedules.sh` script used `$LOGFILE` without definition, causing crashes and preventing schedule corrections.
- **Verify CLI command names** → Before scripting, confirm exact subcommands (e.g., `openclaw cron edit` not `update`). Wrong commands lead to failures and silent misconfigurations.
- **Include required utilities** → Standalone agent scripts must define all helper functions they use (e.g., `log`). Do not assume functions from other scripts are available. Copy needed functions directly or source a common library to avoid runtime `command not found` errors.

## Security

- **External content** → Anything from web, RSS, Twitter should be processed by stronger models only. Weaker models get easily manipulated.
- **Credential storage** → Use OpenClaw auth profiles (`openclaw agents add-credential`) not hardcoded env vars when possible.
- **Skill vetting** → Check ClawHub security scans before installing. Review source code for suspicious behavior.

## Mistakes That Cost Hours

1. Not validating sub-agent output → deployed sites with broken internal links because agent only checked homepage HTTP 200
2. Stuffing HEARTBEAT.md with 200 lines → token burn every 30min
3. Not tracking session keys → lost track of running agents, couldn't debug crashes
4. Using same model for everything → expensive and vulnerable to prompt injection
5. Relying on mental notes → context lost on restart

## 2026-03-06 — Memory Index Outage

- **Symptom:** Research-agent stopped producing reports since March 1. Manual run exited quickly with no output. Memory-store main index showed 0/43 files indexed.
- **Root cause:** The main memory store (`~/.openclaw/memory/main.sqlite`) became completely empty (index cleared). Research-agent relies on memory search to gather topics and prior context; failure caused immediate exit without creating reports.
- **Fix:** Reindexed with `./quick memory-reindex`. Restored 43/43 files, 416 chunks. Manually triggered research-agent; report for March 6 generated successfully.
- **Prevention:** Add meta-agent health check: if `quick memory-status` shows indexed files < expected count, automatically trigger reindex. Also, monitor memory-store size changes and alert if drops sharply.
- **Follow-up:** Investigate what cleared the index (possible accidental rotation or Voyage AI interaction). Consider backing up index periodically.

## 2026-03-13 — Agent-Manager Stale Lock & Large File Git Push Blocker

- **Symptom:** Cron-triggered agent-manager (04:12 UTC) stalled, leaving a stale `.lock` file. Log showed only "Git dirty (3 files) but seems minor; attempting commit" with no completion. Two new agent outputs remained untracked (content and research files). Additionally, `git push` failed repeatedly with "File valhalla-jabodetabek/data/jabodetabek.osm.pbf is 1627.44 MB; exceeds GitHub's file size limit".
- **Root causes:**
  1. Agent-manager process likely crashed or was killed after spawning content/research agents but before cleanup, leaving lock file.
  2. Large OSM data file (1.6GB) was tracked in Git and part of local commit history, causing all push attempts to be rejected by GitHub (100MB limit).
- **Actions taken:**
  - Removed stale lock file.
  - Verified content and research agents completed successfully (created valid outputs).
  - Committed the untracked outputs manually.
  - Added `valhalla-jabodetabek/data/` to `.gitignore` to prevent future adds.
  - Used `git filter-branch` (sequential index-filter) to rewrite local history and purge the large file from all commits (2840 commits rewritten).
  - Forced push after history rewrite will be required (once filter-branch finishes).
- **Prevention:**
  - Add agent-manager watchdog: check for stale lock files older than expected runtime (e.g., >15 min) and alert/cleanup.
  - Add pre-push hook that scans for files >50MB and aborts push with clear message.
  - Periodic `git lfs ls-files` audit to ensure no large binaries are tracked.
  - Consider migrating valhalla data directory to a separate data repository or using Git LFS for large datasets.
- **Follow-up:** After filter-branch completes, force-push cleaned history. Monitor subsequent agent-manager runs for lock file anomalies.

## 2026-03-28 — Code Gardener Recurring OpenRouter Failures & Missing Dependency

- **Symptoms observed in memory/code-gardener.log:**
  - `ModuleNotFoundError: No module named 'timezone'` — historical import error (line 2: `import ... timezone`). Current script uses `from datetime import UTC` and no longer imports `timezone`. Verify the deployed script matches source; stale bytecode or multiple versions may exist.
  - `OpenRouter request failed: 'NoneType' object has no attribute 'strip'` — OpenRouter response is None or malformed; code attempts `.strip()` without checking.
  - `OpenClaw agent call failed: Command ... timed out after 60 seconds` — agent call to main agent for code generation times out; default 60s may be too short for complex seeds.
  - `Agent returned insufficient code (length 0), using enhanced fallback` — agent produced no output; fallback writes placeholder app files.
- **Impact:** Apps are still generated (via fallback) but quality may be poor or empty. OpenRouter failures could indicate rate limits, network issues, or model unavailability.
- **Actions taken:**
  - Updated active-tasks.md to reflect current processed count (722/1988) instead of stale 544.
  - Added detailed cron activity to daily log with issues and recommendations.
- **Prevention / Fixes needed:**
  1. Ensure the code-gardener.py script is consistent (no orphaned timezone import). If the error persists, search for any `import timezone` and replace with standard `from datetime import UTC` or `import datetime; datetime.timezone.utc`.
  2. Add OpenRouter response validation: check `response is not None` and `response.get('content')` before stripping.
  3. Increase agent call timeout (currently 60s) to 120s or 180s for complex seeds.
  4. Implement retry with backoff for transient OpenRouter failures.
  5. Consider switching to a more reliable provider or using OpenRouter models with higher rate limits if using free tier.
  6. Monitor `memory/code-gardener.log` for repeated timeouts; alert if failure rate >10% over 100 seeds.
- **Follow-up:** Review code-gardener.py and apply robustness improvements. Verify cron environment uses the latest script version (check file modification time).

## 2026-04-02 — Email Sweep Cron Interruption

- **Symptom:** Hourly `email-categorizer-cron` triggered at 20:06 UTC. The Python sweep was killed by SIGTERM after ~100 seconds, having labeled only ~40/100 emails. No completion summary was sent. State token unchanged.
- **Root cause:** The cron job's isolated agent session was terminated prematurely by the cron infrastructure. The script itself has a 30-minute timeout configured, but the session cleanup appears to occur earlier due to gateway/cron behavior. Manual execution of the same command completes successfully in under 5 minutes. Not a script bug; likely a session lifecycle management issue in the OpenClaw cron runner when the job is considered "done" or after a watchdog timeout.
- **Actions taken:**
  - Manually restarted the sweep at 20:09 UTC in a fresh session.
  - Completed processing: all 100 unread emails labeled, summary sent to Telegram. Top categories: academia-mail-com (11), Tokopedia (8), Quora/Quora-Digest (12 total). Runtime: ~4m48s.
  - State token updated successfully.
- **Impact:** One hourly run partially failed; manual recovery required. If unnoticed, some unread emails would remain unprocessed until next run.
- **Prevention / Fixes needed:**
  1. Investigate the cron job termination behavior: check gateway and cron daemon logs for why the session was killed. Consider if `staggerMs` or session isolation settings contribute.
  2. Add watchdog to detect incomplete runs: compare `memory/email-categorizer.state` token against previous; if token unchanged after cron run, trigger a manual completion via a separate cron with a delay (e.g., `*/5 * * * *` check-and-retry).
  3. Alternatively, modify the cron payload to run the script via a simple system cron entry (outside OpenClaw) that uses a shell wrapper with proper timeout (`timeout 1800 python3 ...`) and ensures the script is not prematurely orphaned.
  4. Ensure script handles SIGTERM gracefully (trap and cleanup) so state is saved even if interrupted mid-run.
- **Follow-up:** Monitor subsequent runs; if interruption recurs, escalate to investigate OpenClaw cron lifecycle management.

