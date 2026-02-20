# Workspace Builder Findings — 2026-02-20

**Initial Assessment Report**  
**Session:** workspace-builder (cron-triggered)  
**Timestamp:** 2026-02-20 17:00 UTC

---

## System Overview

- **OS:** Linux 6.17.0-1007-oracle (arm64)
- **Gateway:** healthy (port 18789)
- **Disk:** 44% used (healthy)
- **Memory system:** local FTS+ (Voyage AI disabled)
- **Git:** clean, up-to-date with origin/master
- **Active agents:** none (all validated/cleaned)
- **Cron jobs:** 22 OpenClaw cron jobs, all documented; validation active every 30 min

---

## Current Blocker: Research Hub Deployment

The Research Hub web application (`apps/research-hub/`) is scaffolded and ready but **cannot be automatically deployed** because the necessary CLI tools (`gh`, `vercel`) are not in the OpenClaw exec-allowlist.

### Why This Matters

- User's interests shifted to **tech infrastructure** (per USER.md update on 2026-02-20)
- Research Hub is a Next.js portal for browsing research reports — a tech showcase
- Deployment automation would provide immediate tangible output and a reusable pattern

### Technical Details

- **Exec-allowlist location:** `~/.openclaw/exec-approvals.json` (OpenClaw Gateway config)
- **Current allowlist entries for `main` agent:** includes `git`, `openclaw`, `bash`, `jq`, etc. (24 entries)
- **Missing:** `gh` (GitHub CLI) and `vercel` (Vercel CLI)
- **Setup script ready:** `apps/research-hub/setup-standalone-repo.sh` requires `gh` and `vercel`
- **Note:** The user must also have `gh` authenticated and `vercel` installed on the system. The allowlist only permits execution; it does not install the tools.

### Path to Enablement

1. Add allowlist entries for:
   - `/usr/bin/gh` (common location; could also be `/usr/local/bin/gh` or `~/.npm-global/bin/gh`)
   - `/usr/local/bin/vercel` or `~/.npm-global/bin/vercel` (depends on npm global prefix)
2. Restart OpenClaw gateway to apply the new allowlist
3. Run setup script: `./apps/research-hub/setup-standalone-repo.sh` either manually or via a quick launcher

---

## Other Observations

### Strengths
- Robust cron validation in place (`scripts/validate-cron-schedules.sh`)
- Good observability via `quick` commands (health, cron, memory, disk)
- Active tasks registry well-maintained (<2KB)
- Comprehensive lessons learned in `lessons.md`

### Minor Gaps
- No dedicated `quick` commands for Research Hub status/deploy (can add)
- Deployment guide not yet documented (create `docs/research-hub-deployment.md`)
- `quick` launcher is extensive; some research/content commands might be missing from help summary? (the full help is long; but the script covers them)

---

## Quick Health Snapshot

```
$ ./quick health
Disk OK 44% | Updates: none | Git clean (0 changed) | Memory: 18f/81c (clean) local FTS+ | Reindex: 4.1d ago | Gateway: healthy | Downloads: 13 files, 3.3G
```

**Cron status:** last supervisor-cron run (18:10 UTC) OK, all jobs healthy.

**Memory stores:** local SQLite only, no Voyage AI rate limits.

---

## Proposed Improvements (from task_plan.md)

1. **Enable Research Hub deployment** by extending exec-allowlist and adding quick wrappers
2. **Improve Research Hub monitoring** with status command
3. **Document deployment procedure** in a dedicated guide
4. **Ensure system validation** passes post-implementation

---

**Next:** Execute implementation tasks in `task_plan.md`, update `progress.md` as we go.
