# OpenClaw Fresh Install Task List

**Goal**: Reinstall OpenClaw cleanly while preserving the workspace and assistant identity.

**Prerequisite**: Back up `~/.openclaw/workspace/` and `~/.openclaw/memory/` before starting.

---

## Phase 1: Pre‑Installation

- [ ] Verify workspace backup exists:
  ```bash
  tar czf ~/openclaw-backup-$(date +%F).tar.gz ~/.openclaw/workspace ~/.openclaw/memory
  ```
- [ ] Document current configuration:
  ```bash
  openclaw --version > ~/openclaw-version.txt
  openclaw gateway status > ~/gateway-status.txt
  openclaw cron list --json > ~/cron-backup.json 2>/dev/null || true
  ```
- [ ] Export list of installed skills:
  ```bash
  ls -1 ~/.openclaw/workspace/skills/ > ~/skills-list.txt
  ```
- [ ] Save channel configuration (Telegram token, chat IDs):
  ```bash
  cp ~/.openclaw/openclaw.json ~/openclaw-config-backup.json
  ```

---

## Phase 2: Uninstall Old OpenClaw

- [ ] Stop gateway:
  ```bash
  systemctl --user stop openclaw-gateway.service
  ```
- [ ] Remove npm package:
  ```bash
  npm uninstall -g openclaw
  ```
- [ ] Optionally remove config (will lose cron & credentials):
  ```bash
  # KEEP workspace/ and memory/ if you want to preserve assistant
  rm -rf ~/.openclaw/cron ~/.openclaw/devices ~/.openclaw/exec-approvals.json
  # Or remove everything except workspace/memory:
  # mv ~/.openclaw ~/.openclaw.old && mkdir ~/.openclaw && mv ~/.openclaw.old/workspace ~/.openclaw/ && mv ~/.openclaw.old/memory ~/.openclaw/
  ```

---

## Phase 3: Install OpenClaw

- [ ] Install npm package globally:
  ```bash
  npm install -g openclaw
  ```
- [ ] Verify installation:
  ```bash
  openclaw --version
  ```
- [ ] Initialize (if needed):
  ```bash
  openclaw gateway --dev  # only if ~/.openclaw does not exist
  ```
- [ ] Restore credentials (if you backed up `auth-profiles.json` or have API keys):
  ```bash
  # Re-add Voyage AI, OpenAI, etc. via openclaw agents add-credential
  openclaw agents add-credential --provider voyage --api-key YOUR_KEY
  ```
- [ ] Re‑install essential skills (if not in workspace):
  ```bash
  # From ClawHub:
  clawhub install edge-tts
  clawhub install anime-lookup
  # Manual skills already in workspace/skills/ will be auto‑loaded
  ```

---

## Phase 4: Restore Workspace

- [ ] If you moved workspace back:
  ```bash
  # Ensure ownership
  chown -R ubuntu:ubuntu ~/.openclaw/workspace
  ```
- [ ] Re‑link memory database if needed:
  ```bash
  # Memory is in ~/.openclaw/memory/; if you kept it, nothing to do
  ```
- [ ] Install quick launcher if missing:
  ```bash
  # The `quick` script lives in workspace root; ensure it's executable
  chmod +x ~/.openclaw/workspace/quick
  ```
- [ ] Verify config (Telegram, etc.):
  ```bash
  openclaw gateway status
  ```

---

## Phase 5: Recreate Cron Jobs

**OpenClaw cron does not survive uninstall**; recreate all jobs:

- [ ] **workspace‑builder** (every 2h Bangkok):
  ```bash
  openclaw cron add --name workspace-builder --schedule '0 */2 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --model openrouter/stepfun/step-3.5-flash:free --timeout 600
  ```
  *(Set appropriate prompt via config or edit after)*

- [ ] **email‑cleaner‑cron** (09:00 Bangkok):
  ```bash
  openclaw cron add --name email-cleaner-cron --schedule '0 9 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'quick email-clean' --timeout 600
  ```

- [ ] **auto‑torrent‑cron** (02:00 Bangkok):
  ```bash
  openclaw cron add --name auto-torrent-cron --schedule '0 2 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'quick nyaa-top --limit 10 --max-size 2G --add' --timeout 600
  ```

- [ ] **random‑torrent‑downloader** (every 2h UTC):
  ```bash
  openclaw cron add --name random-torrent-downloader --schedule '0 */2 * * *' --timezone UTC \
    --payload 'agentTurn' --command 'bash /home/ubuntu/.openclaw/workspace/cron/torrent-downloader.sh' --timeout 600
  ```

- [ ] **traffic‑report‑cron** (22:00 UTC):
  ```bash
  openclaw cron add --name traffic-report-cron --schedule '0 22 * * *' --timezone UTC \
    --payload 'agentTurn' --command 'bash /home/ubuntu/.openclaw/workspace/traffic_report.sh' --timeout 600
  ```

- [ ] **content‑index‑update‑cron** (05:30 Bangkok):
  ```bash
  openclaw cron add --name content-index-update-cron --schedule '30 5 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'quick content-index-update >> memory/content-index-cron.log 2>&1' --timeout 600
  ```

- [ ] **memory‑reindex‑cron** (Sun 04:00 Bangkok):
  ```bash
  openclaw cron add --name memory-reindex-cron --schedule '0 4 * * 0' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'quick memory-index >> memory/memory-reindex.log 2>&1' --timeout 600
  ```

- [ ] **log‑rotate‑cron** (Sun 05:00 Bangkok):
  ```bash
  openclaw cron add --name log-rotate-cron --schedule '0 5 * * 0' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'quick log-rotate >> memory/log-rotate.log 2>&1' --timeout 600
  ```

- [ ] **dev‑agent‑cron** (20‑min intervals 08:00–22:00 Bangkok):
  ```bash
  openclaw cron add --name dev-agent-cron --schedule '0,20,40 8-22 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'bash -c '\''cd /home/ubuntu/.openclaw/workspace && ./agents/dev-cycle.sh >> dev-agent.log 2>&1'\''' --timeout 600
  ```

- [ ] **content‑agent‑cron** (10‑min intervals 08:00–22:00 Bangkok):
  ```bash
  openclaw cron add --name content-agent-cron --schedule '0,10,20,30,40,50 8-22 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'bash -c '\''cd /home/ubuntu/.openclaw/workspace && ./agents/content-cycle.sh >> content-agent.log 2>&1'\''' --timeout 600
  ```

- [ ] **research‑agent‑cron** (15‑min intervals 08:00–22:00 Bangkok):
  ```bash
  openclaw cron add --name research-agent-cron --schedule '0,15,30,45 8-22 * * *' --timezone Asia/Bangkok \
    --payload 'agentTurn' --command 'bash -c '\''cd /home/ubuntu/.openclaw/workspace && ./agents/research-cycle.sh >> research-agent.log 2>&1'\''' --timeout 900
  ```

**Note**: The agent prompts (the "You are the dev-agent..." text) are stored in the agent configuration. If the agents are defined in `openclaw.json` under `agents.list`, the cron payload just needs to trigger the cycle script. Ensure `agents/dev-cycle.sh`, `agents/content-cycle.sh`, `agents/research-cycle.sh` exist and are executable.

---

## Phase 6: Verify Installation

- [ ] Start gateway:
  ```bash
  openclaw gateway start
  ```
- [ ] Check status:
  ```bash
  openclaw gateway status
  quick health
  ```
- [ ] List cron jobs:
  ```bash
  openclaw cron list
  ```
- [ ] Run a test job manually:
  ```bash
  openclaw cron run --job dev-agent-cron
  ```
- [ ] Verify agent logs:
  ```bash
  tail -f dev-agent.log
  ```
- [ ] Ensure memory search works:
  ```bash
  quick search "test"
  ```
- [ ] Check content and research indexes:
  ```bash
  cat content/INDEX.md
  cat research/INDEX.md
  ```

---

## Phase 7: Post‑Install Tasks

- [ ] Commit any new changes to GitHub:
  ```bash
  git add -A
  git commit -m "chore: restore after fresh OpenClaw install"
  git push
  ```
- [ ] Update `active-tasks.md` to reflect current agent status (cron jobs running)
- [ ] Schedule a weekly memory reindex if not already cron'd
- [ ] Consider enabling `sudo` for passwordless operations if needed (`./setup-sudo.sh`)
- [ ] Test `quick gateway-fix` if gateway becomes unstable

---

## 8. Optional Utilities

If missing, add these quick commands (edit `quick`):
- `gateway-status` (already implemented)
- `gateway-fix` (already implemented)
- `verify` (comprehensive check)
- `daemons` (show running agents)
- `time`, `holidays`, `anime`, etc.

---

## 9. What to Keep vs Reinstall

| Item | Keep across reinstall? | Reason |
|------|----------------------|--------|
| `~/.openclaw/workspace/` | **YES** | Contains all your files, agents, scripts, configs, and the assistant's "soul" |
| `~/.openclaw/memory/` | **YES** | Persistent memory database (SQLite) |
| `~/.openclaw/cron/` | NO (recreate) | Cron jobs are stored here but must be re-added via `openclaw cron add` |
| `~/.openclaw/devices/` | NO (re‑pair) | Device tokens will be invalid; re‑pair Telegram/Discord |
| `~/.openclaw/credentials/` | Re‑add API keys | Credentials are encrypted per install; re‑enter Voyage, OpenAI, etc. |
| `~/.openclaw/openclaw.json` | Partially keep | Keep channel configs, but agent definitions may need refresh |
| `~/.openclaw/exec-approvals.json` | NO | Approvals are ephemeral |

---

## 10. Quick Reference Commands

```bash
# Gateway
openclaw gateway start|stop|restart|status
openclaw devices list
openclaw devices rotate --role operator --device <id>

# Cron
openclaw cron list
openclaw cron add ...  # see Phase 5
openclaw cron run --job <name>
openclaw cron remove --job <name>

# Agent control
openclaw sessions list
openclaw sessions kill --sessionKey <key>

# Workspace
./quick health
./quick verify
./quick gateway-status
./quick gateway-fix
```

---

**End of Task List**

Tick each box as you complete. After fresh install, monitor for a few days to ensure all agents and cron jobs are running as expected. (◕‿◕)♡
