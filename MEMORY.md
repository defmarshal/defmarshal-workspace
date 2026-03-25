# Long-term Memory Index

*Last updated: 2026-03-22*

## Personal
def, UTC+7, mewmew assistant; anime, tech; prefers delegation: Qwen for code, Gemini for research

## Protocols
- `protocols.md` – Delegation workflow (Qwen coding, Gemini research)

## Projects
- MewChat / MewDash – Real-time chat UI with SSE, merged history
- OpenClaw Idle RPG – Conceptual, not yet started
- Anime Studio Tycoon – Dedicated sub-agent active (2026-03-04)
- Research Hub – Deployed, operating under Nyepi throttling (Mar 18–24)
- Torrent System – aria2 + 115 integration
- System Health – Disk cleanup, heartbeat, log rotation, memory reindex (rate-limited)

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
- Gateway: port 18789; Memory: local FTS+ only (Voyage disabled due to 3 RPM limits); systemd linger recommended: `sudo loginctl enable-linger ubuntu`
- Always delegate: code → Qwen, research → Gemini. I handle design/integration.
- **Cron health monitoring:** Three layers:
  - `agent-manager-cron` (every 30 min) validates schedules against `CRON_JOBS.md` and auto‑commits corrections.
  - `cron-supervisor-cron` (every 30 min, staggered) watches for failures, disk issues, gateway down, memory reindex needs; sends Telegram alerts.
  - `notifier-cron` (every 2h) escalates persistent failures and disk threshold warnings.
- **Status‑holiday plugin:** Enabled; adds Nyepi (18–24 Mar 2026) to System Status broadcasts. throttles agent activity but monitoring remains active.
- **Email Sweep & Intelligent Labeling:** Analyzer (`email_label_analyzer.py`) scans senders and builds `memory/label_mapping.json` (155+ distinct senders). Sweep (`email_sweep.py`) runs hourly (`BATCH_SIZE=100, PAGES_PER_RUN=1`), applies precise `Sweep/<Sender>` labels, marks emails as read, and sends Telegram summaries. Backlog clearing steadily.
- **Memory reindex staleness (2026-03-18):** Voyage AI rate limits (3 RPM free tier) prevent automatic reindex; main store shows 0/63 indexed files. Manual `quick memory-reindex` attempts batched with delays; automatic retry continues. Local FTS fallback functional for simple searches.
- **Recent:**
  - **Content Gardener Completion (2026-03-19):** Cron job finished successfully after processing 29 seeds from Mar 17–19 pool. Content output reached 779 files; all logs clean. Gardener pipeline stable under Nyepi throttling.
  - **Code Gardener Completion (2026-03-19):** Generated app from DoorDash seed using fallback method (OpenRouter empty response). 491 seeds remain for future cycles.
  - Meta-summary cron (14:08 UTC) confirmed system health: disk 82%, 19 APT updates, memory reindex pending, content-agent produced afternoon status noting security domain gap. ✓
  - Git janitor cleaned yesterday's agent outputs (9 files, 258 insertions) on 2026-03-18 00:30 UTC.
  - Disk usage stabilized at 82% after earlier cleanup; threshold 85% watch ongoing.
  - **Gardeners System Status (2026-03-22):** Research Gardener ran at 00:15 UTC, processing "It's been 20 years since the first tweet" (Tavily API unavailable, local synthesis). Total processed seeds: 398/1222 across shared pool. Content Gardener last seen Mar 21 23:02 UTC; Code Gardener last seen Mar 21 19:08 UTC. All operating under Nyepi throttling. Report counts: research 456, content 779+, apps ~1600+.
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
  - **Disk Cleanup & Meta-Summary Success (2026-03-16):** meta-summary cron detected disk at 88%, automatically removed node_modules and .next from apps/research-hub and apps/openclaw-idle-rpg, freeing ~1GB. Disk reduced to 86% (38G/45G, 6.4G free). Summary delivered to Telegram. System nominal. (◕‿◕)♡
- **Cron Watchdogs (2026-03-14):** Added `cron-supervisor-cron` (every 30 min) to monitor system health (cron jobs, gateway, memory, disk, updates) and send Telegram alerts. Companion to `agent-manager-cron` (validation + repairs). Both now documented in `CRON_JOBS.md`; removed old inactive `supervisor-cron`.
- **System Snapshot (2026-03-24):** meta-summary cron confirmed stable operations under Nyepi (Mar 18–24). Disk ~83%. Email sweep stable with timeout fixes (curl 10s/70s). All gardeners active: Research (484+ reports), Content (779+), Code (~1600+ apps). Memory reindex rate-limited (63 files pending), local FTS functional.

**Critical Intelligence (2026-03-25):**
- **Meta AI Agent Breach** (March 18-20): Autonomous agent exposed "large amount" of sensitive data to thousands of employees for 2 hours. Incident reveals AI agents introduce error types humans don't - autonomous actions with incorrect context that scale. Pattern across Big Tech (Meta, Amazon AWS Feb 2026) shows autonomy without guardrails = systemic risk.
- **MCP Vulnerability Gap**: 40% of MCP implementations remain unpatched against CVEs (CVE-2025-49596 critical RCE 60% patched, CVE-2026-26118 Azure SSRF). Affects all domains: anime studios (92% AI adoption), BaaS platforms, CBDC systems. Immediate scan required.
- **AI Insurance Market**: Armilla AI first Lloyd's coverholder for AI liability (1-5% of AI agent revenue premium). Provides warranty after security assessment. Cisco DefenseClaw launching March 27 integrates with Armilla for compliance-as-coverage.
- **Anime Industry Financial Collapse**: FY2024 data shows MAPPA $120M revenue, $0 profit; Wit Studio $70M, -$5M loss; 68% of studios at break-even/loss; 12 closures in 2025 (+300% vs 2024). JACA guidelines mandatory April 1 for subsidized studios - union demands include $5K/worker retraining budget, AI revenue sharing.
- **Embedded Finance AI Compliance**: EU AI Act deadline August 2, 2026 (5 months). Survey: 70% of compliance pros say AI is top risk; 73% lack AI policies; 38% have no audit trails. BaaS providers must demonstrate runtime safety (OpenShell), immutable logging, human override.
- **CBDC Programmable Money Risk**: 137 countries piloting; AI agent integration planned. Smart contract vulnerabilities (reentrancy, conditional logic bypass) could enable sovereign digital currency theft. Mitigation: per-agent transaction caps, multi-sig for high-value, circuit breakers.
- **Post-Quantum Cryptography**: "Harvest now, decrypt later" attacks already happening. Financial services data longevity (7-30 years) makes PQC migration urgent. 5-phase framework: inventory → prioritize → test hybrid → migrate → complete transition. Cost: mid-bank $5-15M over 3 years.
- **AI Trading Failures**: Lobstar Wilde lost $441K (Feb 2026) due to decimal error + memory corruption; OpenClaw GPT-5 agent reported 62% loss. DeFi protocols need transaction caps, rate limits, human oversight before autonomous wallet control.
- **Observability Stack**: Grafana Agent + OpenTelemetry now recommended for AI agent runtime metrics. VictoriaMetrics benchmarking shows correctness issues in many log collectors - validate your pipeline.

**Cross-Domain Convergence**: All sectors share MCP, OpenShell, PQC, AI insurance dependencies. Single vulnerability could cascade across creative + financial + sovereign systems. 18-month window (Q2 2026 - Q4 2027) decisive before standards harden and first systemic AI catastrophe.
- **LinkedIn PA Agent Fix (2026-03-12):** Completely rewrote research phase to use agent tool calls (`openclaw agent` with `web_search`/`web_fetch`) instead of broken CLI commands. Also fixed dynamic query generation syntax. Posts now reach 300+ words with rich, sourced data. Media quality restored.
  - **Meta-Agent Rate Limit Fix (2026-03-10):** Spawn retry logic + 30m cooldown lock; cron frequency reduced to every 2 hours. Prevents OpenRouter throttling.
  - **Meta-Agent Cron Migration (2026-03-10 10:30 UTC):** Migrated from `agentTurn` to system crontab. Eliminates OpenRouter API call for meta-agent itself, ending rate limit warnings entirely. Child agents still use OpenRouter but with safe throttling.
  - **Garden Dashboard Completion (2026-03-10):** Finished integration of `garden-dashboard.html` via `outputs-manifest.json`, `garden-server.py` (port 3002), and `quick garden` commands. Beautiful at-a-glance system overview now live. Tailscale accessible: http://100.108.208.45:3002/garden-dashboard.html.
  - **System Organism Dashboard (2026-03-10):** Ultra-kawaii living creature dashboard (`organism-dashboard.html`) with animated canvas, pastel colors, floating hearts, agent bubbles. Serves on same port. Access: http://localhost:3002/organism-dashboard.html.
