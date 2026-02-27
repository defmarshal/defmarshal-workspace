# Lessons Learned

Recurring patterns, mistakes, and best practices. Load on demand via `memory_search` or direct read when context requires.

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
