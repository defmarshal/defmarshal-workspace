# Findings & Decisions

## Requirements
- Clean memory documentation: remove backup files, manage log retention
- Improve git hygiene: refine .gitignore, ensure transient files not tracked
- Add agents command: enhance `quick agents` with useful options (JSON output, filtering)

## Research Findings
- Current `quick agents` runs `openclaw sessions` and shows human-readable table
- Git status shows: modified: aria2.conf, dev-agent.log; untracked: MEMORY.md.bak, dev-agent-loop.sh, research/ files, skills/aria2/
- .gitignore already excludes *.log, *.session, __pycache__, tts_output, etc.
- Memory directory contains: daily .md files, .jsonl, summary .json, and cron logs (daily-summary-cron.log, email-cleaner-cron.log, workspace-builder.log)
- active-tasks.md tracks all agents; the current workspace-builder task is the one running now.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Remove MEMORY.md.bak | Backup not needed; workspace is under Git |
| Keep all *.log ignored | Already in .gitignore; ensure they remain untracked |
| Add `--json` flag to agents command | Provides machine-readable output; consistent with other quick commands |
| Add `--running` filter to agents | Show only recently active sessions (optional) |
| Do not commit cleanup changes separately | Wait until final build commit to avoid extra history |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| `quick` command not found in non-interactive shell | Use full path `/home/ubuntu/.openclaw/workspace/quick` in scripts and tests |
| Agents output may be too verbose | Consider providing concise mode and JSON mode |

## Resources
- OpenClaw sessions command: `openclaw sessions [--json]`
- .gitignore best practices: ignore logs, sessions, caches, transient state
- quick launcher pattern: subcommands with help and option parsing

## Visual/Browser Findings
- None

---
*Update this file after every 2 view/browser/search operations*