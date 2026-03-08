# HANDOFF TO QWEN — 2026-03-08

**Status:** Partial implementation; 3 tasks remain. Do NOT remove or disrupt existing working parts.

## Workspace & Key Files
- Root: `/home/ubuntu/.openclaw/workspace`
- OpenClaw config: `/home/ubuntu/.openclaw/openclaw.json`
- Cron definitions: `/home/ubuntu/.openclaw/cron/jobs.json`
- Meta-agent script: `agents/meta-agent.sh`
- Email sweep script: Inline within cron payload (`email-categorizer-cron`)
- Systemd: `openclaw-gateway` (user service)

## Completed (Verified)
- Cron pruned to 10 essentials + `evolver-agent-cron` + `email-categorizer-cron` + `meta-agent-cron`.
- `openclaw.json`: only `telegram` + `whatsapp` plugins; removed `wizard`, `msteams`, `clawaifu-selfie`.
- Backup: `workspace-backup-20260306-174418.tar.gz`
- Evolver: `agents/evolver-cycle.sh` running hourly (EVOLVE_STRATEGY=balanced, no `--review`).
- Email sweep: sequential, stateful, categorizes, sends Telegram summary. Test batch 100 → 2 min; categories: alerts:2, banking:23, personal:71, newsletters:2, hr:2. Telegram delivery fails silently; log: `memory/email-categorizer.log`.
- Meta-agent: cron hourly, `delivery: botMessage`, `target: "last"` (posts to chat).

## Tasks to Implement

### Task 1: Throttle Meta-Agent Chat Summaries (Every 6h)
- File: `agents/meta-agent.sh`
- Requirement: Run hourly (spawn agents, check state) but send Telegram summary only every 6 hours.
- Implementation:
  - Add state file: `memory/meta-summary.state` with variable `LAST_SENT_MS`.
  - At script end: `now=$(date +%s); last=${LAST_SENT_MS:-0}; if (( now - last >= 21600 )); then send summary; echo "LAST_SENT_MS=$now" > memory/meta-summary.state; fi`
  - Keep all other hourly logic unchanged.
- Validation: Wait for two runs (<6h apart) and confirm only one Telegram message appears.

### Task 2: Embed Nyepi Holiday in Gateway System Status Broadcast
- The gateway emits periodic "System Status (HH:MM UTC) - Disk: X% - Gateway: healthy ..." messages. These originate from the `openclaw-gateway` process (not a cron).
- Goal: Append "Nyepi 18–24 Mar 2026" to that message.
- Investigation:
  - Search dist for the formatter: `grep -R "System Status" /home/ubuntu/.npm-global/lib/node_modules/openclaw/dist/`
  - If configurable via `openclaw.json` or env, add the holiday string there (preferred).
  - If hard-coded, make minimal patch to the source file (e.g., `index.js` or `gateway-cli-*.js`) to concatenate the holiday note. Keep a diff and be ready to revert.
  - Alternative: implement a `message_sending` plugin hook (if supported) that modifies outbound system status messages.
- Caution: Do not break gateway. After any change, restart: `systemctl --user restart openclaw-gateway` and monitor logs with `journalctl --user -u openclaw-gateway -f`.

### Task 3: Optimize Email Sweep Throughput
- Current inline script in `cron/jobs.json` is sequential with default `BATCH_SIZE=500`, `PAGES_PER_RUN=4`, `MAX_PARALLEL` unused; timeout 1800s. State: `memory/email-categorizer.state`.
- To clear ~15k backlog faster, adjust batch size:
  - Set `BATCH_SIZE=1000` and keep `PAGES_PER_RUN=4` → up to 4000 emails/run.
  - Keep sequential loops (no parallel) to avoid hangs.
  - Ensure `NEXT_PAGE_TOKEN` is saved/loaded correctly.
  - Telegram delivery may still fail; if so, either fix `openclaw message send` path or drop Telegram summary to avoid log noise.
- Suggested safe change: edit `cron/jobs.json` payload to set `BATCH_SIZE=1000` in the inline script. No other logic change needed.
- Test manually with small batch first: `BATCH_SIZE=10` for one run, verify counts, then revert to 1000.

### Optional Task 4: Gmail Skill Integration
- If the user wants to switch from custom sweep to built-in `gmail` skill:
  - Verify Maton connection ID in `skills/gmail` config matches https://ctrl.maton.ai/connections.
  - Ensure OAuth consent complete. Not urgent; custom sweep works.

## Important Notes
- **Do not stop/disable evolver or email sweep** — they are functional.
- Gateway restart required after any dist patch or config change.
- All changes should be committed with clear messages.
- If any step is ambiguous, pause and ask the user before proceeding.
- Rollback plan: restore `workspace-backup-20260306-174418.tar.gz` if something breaks.

## Validation Checklist
- [ ] Meta-agent sends chat messages only every 6h (monitor for 12h).
- [ ] "System Status" messages include "Nyepi 18–24 Mar 2026".
- [ ] Email sweep processes ~4000 emails per run without exceeding 1h (check logs for progress and `NEXT_PAGE_TOKEN` advancement).
- [ ] No new cron jobs removed or disabled.
- [ ] `openclaw-gateway` remains healthy (`systemctl --user status openclaw-gateway`).

---

**Handoff by:** mewmew (assistant)
**Date:** 2026-03-08
**Backup:** `/home/ubuntu/.openclaw/workspace-backup-20260306-174418.tar.gz`
