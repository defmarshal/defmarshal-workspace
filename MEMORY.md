# Long-term Memory Index

*Last updated: 2026-03-10*

## Personal
def, UTC+7, mewmew assistant; anime, tech; prefers delegation: Qwen for code, Gemini for research

## Protocols
- `protocols.md` – Delegation workflow (Qwen coding, Gemini research)

## Projects
- MewChat / MewDash – Real-time chat UI with SSE, merged history
- OpenClaw Idle RPG – Conceptual, not yet started
- Anime Studio Tycoon – Dedicated sub-agent active (2026-03-04)
- Research Hub – Deployed
- Torrent System – aria2 + 115 integration
- System Health – Disk cleanup, heartbeat, log rotation

## Links
- `active-tasks.md` (current work)
- `memory/YYYY-MM-DD.md` (daily logs)
- `lessons.md` (patterns)
- `TOOLS.md` (config)
- `CRON_JOBS.md` (schedules)

## Resources
- Voyage AI: https://dashboard.voyageai.com
- OpenClaw: https://docs.openclaw.ai
- GitHub: defmarshal/defmarshal-workspace

## Notes
- Gateway: port 18789; Memory: local FTS+ only (Voyage disabled); systemd linger recommended: `sudo loginctl enable-linger ubuntu`
- Always delegate: code → Qwen, research → Gemini. I handle design/integration.
- **Cron health monitoring:** Three layers:
  - `agent-manager-cron` (every 30 min) validates schedules against `CRON_JOBS.md` and auto‑commits corrections.
  - `cron-supervisor-cron` (every 30 min, staggered) watches for failures, disk issues, gateway down, memory reindex needs; sends Telegram alerts.
  - `notifier-cron` (every 2h) escalates persistent failures and disk threshold warnings.
- **Status‑holiday plugin:** Enabled; adds Nyepi (18–24 Mar 2026) to System Status broadcasts.
- **Email Sweep & Intelligent Labeling:** Analyzer (`email_label_analyzer.py`) scans senders and builds `memory/label_mapping.json` (155+ distinct senders). Sweep (`email_sweep.py`) runs hourly (`BATCH_SIZE=100, PAGES_PER_RUN=1`), applies precise `Sweep/<Sender>` labels, marks emails as read, and sends Telegram summaries. Backlog clearing steadily.
- Recent:
  - **Agent-Manager Stale Lock & Large File Push Blocker (2026-03-13):** Cron-triggered agent-manager stalled, leaving stale lock; discovery: `valhalla-jabodetabek/data/jabodetabek.osm.pbf` (1.6GB) tracked in Git, causing push rejections (GitHub 100MB limit). Recovered by removing lock, manually committing today's agent outputs, adding file to `.gitignore`, rewriting history with `git filter-branch`, and force-pushing. Large file purged from all 2799+ commits; repository clean. Added prevention: pre-push hook plan, Git LFS audit. Follow-up: monitor agent-manager stability.
  - **Memory index outage (2026-03-06 04:08 UTC):** main store dropped to 0 indexed files, breaking research-agent. Reindexed manually; research pipeline restored, March 6 report generated and deployed. Index now 43/43.
  - **Missing downloads directory & index reset (2026-03-08 06:30 UTC):** `downloads/` directory vanished (likely removed by cleanup script after becoming empty). Memory index showed `0/45 files` (false negative corrected by `./quick memory-reindex`). Restored: downloads dir recreated, memory reindexed to 45/45 files (525 chunks). System returned to full health.
  - **Disk usage spike & recovery (2026-03-05–07):** rose 66% → 81% over 2 days, triggering cleanup. Agent-manager (01:05 UTC) cleaned downloads (7.8G → 4.9G) and meta-summary confirms disk back to 66% by afternoon. System stable.
  - Agent-manager (19:00 UTC) validated all cron schedules; 8 essential cron jobs running. System stable.
  - Meta-agent cycles (2026-03-05 03:07 & 20:01 UTC) confirmed content-agent and research-agent running; system stable at 59% disk.
  - Meta-agent (2026-03-06 11:04 UTC) verified agents; content-agent completed, research-agent produced March 6 report.
  - Disabled `linkedin-pa-agent-cron` (2026-03-04) to align with docs after drift detection.
  - Fixed dashboard cron stuck state via disable/enable reset; Python errors now logged.
  - MewChat evolver timeout monitored; will restart on next 6h cycle (12:00 UTC).
  - Disk history sparkline rebuilding after cron state recovery.
  - Active projects updated; anime-studio-tycoon sub-agent running.
  - Voyage AI rate limits persist; memory learning disabled; local FTS active.
  - Meta-supervisor daemon removed (2026-03-06 08:27); cron-supervisor agent removed (08:45). No more periodic "System Status" broadcasts.
  - **Elevated Exec Autonomy (2026-03-10):** `mewmew` agent granted full exec permissions (`tools.elevated.enabled: true`, excluded from `approvals.exec.agentFilter`). Enables autonomous system operations without manual approval.
  - **Cron Delivery Recovery (2026-03-14):** Fixed `cron-supervisor-cron` delivery error (multiple channels) by setting explicit `channel: telegram`. Cleared stale `runningAtMs` on `notifier-cron`. All cron jobs now healthy and monitoring active.
- **Cron Watchdogs (2026-03-14):** Added `cron-supervisor-cron` (every 30 min) to monitor system health (cron jobs, gateway, memory, disk, updates) and send Telegram alerts. Companion to `agent-manager-cron` (validation + repairs). Both now documented in `CRON_JOBS.md`; removed old inactive `supervisor-cron`.
- **LinkedIn PA Agent Fix (2026-03-12):** Completely rewrote research phase to use agent tool calls (`openclaw agent` with `web_search`/`web_fetch`) instead of broken CLI commands. Also fixed dynamic query generation syntax. Posts now reach 300+ words with rich, sourced data. Media quality restored.
  - **Meta-Agent Rate Limit Fix (2026-03-10):** Spawn retry logic + 30m cooldown lock; cron frequency reduced to every 2 hours. Prevents OpenRouter throttling.
  - **Meta-Agent Cron Migration (2026-03-10 10:30 UTC):** Migrated from `agentTurn` to system crontab. Eliminates OpenRouter API call for meta-agent itself, ending rate limit warnings entirely. Child agents still use OpenRouter but with safe throttling.
  - **Garden Dashboard Completion (2026-03-10):** Finished integration of `garden-dashboard.html` via `outputs-manifest.json`, `garden-server.py` (port 3002), and `quick garden` commands. Beautiful at-a-glance system overview now live. Tailscale accessible: http://100.108.208.45:3002/garden-dashboard.html.
  - **System Organism Dashboard (2026-03-10):** Ultra-kawaii living creature dashboard (`organism-dashboard.html`) with animated canvas, pastel colors, floating hearts, agent bubbles. Serves on same port. Access: http://localhost:3002/organism-dashboard.html.
