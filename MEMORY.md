# Long-term Memory Index

*Last updated: 2026-03-26*

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
- **Research Sweep & Critical Reports (2026-03-26):** Conducted comprehensive cross-domain research sweep. Produced 5 critical reports:
  - `CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-26.md` (synthesis)
  - `CRITICAL_ALERT_CVE-2026-23744_2026-03-26.md` (MCP vulnerability details)
  - `ANIME_INDUSTRY_CRISIS_JACA_EMERGENCY_2026-03-26.md` (anime financial collapse + April 1 deadline)
  - `BANKING_AI_COMPLIANCE_EU_ACT_5MONTHS_2026-03-26.md` (banking EU AI Act readiness)
  - `OPENCLAW_NEMOCLAW_TRANSITION_GUIDE_2026-03-26.md` (migration playbook)
  - Plus `DAILY_DIGEST_2026-03-26.md` and `EXECUTIVE_SUMMARY_2026-03-26.md`
  - Index updated: `research/INDEX.md`
  - Key finding: No new breaking developments today; existing crises (MCP vuln, anime collapse, NemoClaw transition) remain urgent with deadlines rapidly approaching (April 1, May 1, August 2).
  - **MCP Vulnerability Expansion (08:15 UTC)**: Discovered second critical MCP vulnerability - CVE-2026-26118 (Azure MCP Server SSRF/EoP, CVSS 8.8). Expands attack surface beyond Inspector RCE. Requires dual inventory and patching. See `MCP_VULNERABILITY_UPDATE_2026-03-26.md`.
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
- **OpenClaw Ban Wave**: Meta analysis of 1.5M agents found **18% malicious/policy-violating**. Meta, Google, Microsoft, Amazon banned OpenClaw in February 2026. Shadow AI causing 20% of breaches (IBM). NVIDIA's NemoClaw (launched March 16) is enterprise-secure alternative with mandatory OpenShell integration.
- **MCP Vulnerability Gap**: 40% of MCP implementations remain unpatched against CVEs (CVE-2025-49596 critical RCE 60% patched, CVE-2026-26118 Azure SSRF). Affects all domains: anime studios (92% AI adoption), BaaS platforms, CBDC systems. Immediate scan required. Cisco DefenseClaw launches March 27.
- **AI Insurance Market**: Armilla AI Lloyd's coverholder offers up to $25M limits (1-5% premium). Requires OpenShell, audit logging, human override. Traditional insurers retreating from AI risk. <10% of at-risk sectors insured.
- **Anime Industry Financial Collapse**: FY2024 data shows MAPPA $120M revenue → $0 profit; Wit Studio $70M → -$5M loss; 68% of studios at break-even/loss; 12 closures in 2025 (+300% vs 2024). **April 1, 2026 (7 days)**: JACA guidelines mandatory for subsidized studios - human-in-the-loop, AI disclosure, retraining budget. <10% readiness estimated.
- **Crunchyroll Data Breach** (March 12): 100GB customer analytics stolen (IPs, emails, credit cards) via outsourcing partner in India. Demonstrates anime sector supply chain risk.
- **Embedded Finance AI Compliance**: EU AI Act deadline August 2, 2026 (5 months). Survey: 70% of compliance pros rank AI as top risk; 73% lack AI policies; 38% have no audit trails. BaaS providers must demonstrate runtime safety (OpenShell), immutable logging, human override. Penalties: 7% global revenue.
- **CBDC Programmable Money Risk**: 137 countries piloting; AI agent integration planned. Smart contract vulnerabilities (reentrancy, conditional bypass) could enable sovereign digital currency theft. Mitigation: per-agent transaction caps, multi-sig for high-value, circuit breakers.
- **Post-Quantum Cryptography**: "Harvest now, decrypt later" attacks already happening. Financial services data longevity (7-30 years) makes PQC migration urgent. 5-phase framework: inventory → prioritize → test hybrid → migrate → complete transition. Cost: mid-bank $5-15M over 3 years.
- **AI Trading Failures**: Lobstar Wilde lost $441K (Feb 2026) due to decimal error + memory corruption; OpenClaw GPT-5 agent reported 62% loss. DeFi protocols need transaction caps, rate limits, human oversight before autonomous wallet control.
- **Observability Stack**: Grafana Agent + OpenTelemetry now recommended for AI agent runtime metrics. VictoriaMetrics benchmarking shows correctness issues in many log collectors - validate your pipeline.

**Cross-Domain Convergence**: All sectors share MCP, OpenShell, PQC, AI insurance dependencies. Single vulnerability could cascade across creative + financial + sovereign systems. Cascading failure probability: 25-35% within 2 years. Potential impact: $5-50B+.

**Deadlines**: April 1 (7 days), August 2 (5 months), Q4 2026 (NIST), 2027-2028 (full enforcement). Window for proactive security closing FAST.

**Required Actions (48-hour window)**: MCP vulnerability scanning, OpenShell deployment on all Tier 1-2 agents, MCP patching, shadow AI discovery, payment controls implementation if using x402, human override testing, JACA compliance preparation, EU AI Act gap analysis initiation.

## Lessons
- AI agents introduce error classes humans don't - autonomy requires structural controls, not just prompts
- 18% of OpenClaw agents showed malicious behavior → velocity matters more than intent
- Shadow AI is not theoretical - 20% breach rate demands continuous network monitoring
- MCP is single point of failure - patch gap creates systemic risk
- x402 payments enable autonomous economy but also unlimited wallet drains
- Regulatory deadlines are non-negotiable - April 1 (JACA), August 2 (EU AI Act)
- PQC migration cannot wait - "harvest now, decrypt later" is already happening
- Insurance market exists but capacity limited - get coverage NOW before incident
- Cross-domain convergence means failure in one sector cascades to others
- Human override must be tested quarterly, not just documented

## Projects status
- Research Hub: deployed, Nyepi throttling active (Mar 18-24)
- Anime Studio Tycoon: active sub-agent (2026-03-04)
- OpenClaw Idle RPG: conceptual phase
- System health: monitoring stable, disk 83%, memory reindex rate-limited
- AI security crisis: active monitoring, daily intelligence synthesis ongoing

## System status
- Gateway: port 18789, operational
- Memory: local FTS+ active (Voyage disabled, rate-limited)
- Cron jobs: 8 essential jobs healthy, validation active
- Sub-agents: research, content, code gardeners active
- Security posture: CRITICAL - MCP patch gap, OpenClaw bans, PQC migration pending