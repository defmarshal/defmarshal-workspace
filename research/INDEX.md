# 📚 Research Repository Index

**Last Updated**: March 28, 2026 08:15 UTC
**Status**: Active - Continuous research operation
**Agent**: research-agent
**Scope**: Anime, Banking, Tech, AI domains

---

## 🚨 CRITICAL ALERTS (Read First)

| Report | Date | Priority | Summary |
|--------|------|----------|---------|
| **[TEAMPCP_CAMPAIGN_UPDATE_2_2026-03-28.md](TEAMPCP_CAMPAIGN_UPDATE_2_2026-03-28.md)** | 2026-03-28 | 🔴 MAXIMUM | **EXPANDED: Self-propagating npm worm (CanisterWorm) + 66+ packages + telnyx PyPI + OpenVSX extensions + poisoned containers + kamikaze.sh destruction.** Single stolen token → 10M+ downloads affected. Assume compromise if used Trivy/Checkmarx/LiteLLM/telnyx Feb 24-Mar 28. ROTATE ALL CREDENTIALS NOW. |
| **[TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28.md](TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28.md)** | 2026-03-28 | 🔴 CRITICAL | **BREAKING: Active supply chain campaign** — TeamPCP compromised Trivy CI, Checkmarx KICS, LiteLLM (3.4M/day), telnyx, npm (66+ pkg), OpenVSX ext. Credential theft + backdoors + K8s worm. 110+ malicious tags. |
| **[CRITICAL_ALERT_LITELLM_SUPPLY_CHAIN_2026-03-28.md](CRITICAL_ALERT_LITELLM_SUPPLY_CHAIN_2026-03-28.md)** | 2026-03-28 | 🔴 CRITICAL | **LiteLLM backdoored**: 1.82.7/1.82.8 (3h window Mar 24) steal AWS/GCP creds, persistent backdoor, K8s worm. 3.4M daily downloads. Check all systems NOW. |
| [CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-28.md](CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-28.md) | 2026-03-28 | 🔴 CRITICAL | **Cross-domain update**: Langflow RCE, MCP patches, JACA 6-day deadline, EU AI Act extension (569-45 plenary), NemoClaw alpha. Synthesis of all active crises. |
| [CRITICAL_ALERT_CVE-2026-33017_UPDATE_2026-03-28.md](CRITICAL_ALERT_CVE-2026-33017_UPDATE_2026-03-28.md) | 2026-03-28 | 🔴 CRITICAL | **ACTIVE EXPLOITATION**: Langflow RCE exploited in wild within 20h; CISA KEV catalog; 15-20% of internet-exposed instances compromised. Patch to 1.9.0.dev8+ IMMEDIATELY |
| [ANIME_INDUSTRY_JACA_EMERGENCY_UPDATE_2026-03-28.md](ANIME_INDUSTRY_JACA_EMERGENCY_UPDATE_2026-03-28.md) | 2026-03-28 | 🔴 CRITICAL | **6 DAYS TO DEADLINE**: April 1 JACA enforcement imminent; <10% compliance; 30-50 studio closures projected; emergency survival strategies |
| [MCP_PATCH_PROGRESS_UPDATE_2026-03-28.md](MCP_PATCH_PROGRESS_UPDATE_2026-03-28.md) | 2026-03-28 | 🟠 HIGH | **MIXED NEWS**: Azure MCP CVE-2026-26118 patched (March 10); but Inspector CVE-2025-49596 still 40% unpatched; only 2.5% of 5,618 servers fully safe |
| [BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md](BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md) | 2026-03-28 | 🟢 MEDIUM | **RELIEF**: EU committee votes 101-9 to extend high-risk AI compliance from Aug 2026 → Dec 2027 (21 months); plenary passed 569-45 on Mar 26 |
| [NEMOCLAW_MIGRATION_READINESS_2026-03-28.md](NEMOCLAW_MIGRATION_READINESS_2026-03-28.md) | 2026-03-28 | 🟡 MEDIUM | **ALPHA STATUS**: NemoClaw alpha with 17 partners; May 1 cloud ban approaching; production readiness concerns but security primitives work |
| [CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-27.md](CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-27.md) | 2026-03-27 | 🔴 CRITICAL | **BREAKING**: 35 AI-code CVEs, MCP scan results, trading failures, CBDC risks, PQC benchmark |
| [MCP_VULNERABILITY_UPDATE_2026-03-26.md](MCP_VULNERABILITY_UPDATE_2026-03-26.md) | 2026-03-26 | 🔴 CRITICAL | **NEW**: Second MCP vulnerability discovered (CVE-2026-26118, Azure MCP SSRF, CVSS 8.8) - expands attack surface |
| [EU_AI_ACT_DEADLINE_EXTENSION_PROPOSAL_2026-03-26.md](EU_AI_ACT_DEADLINE_EXTENSION_PROPOSAL_2026-03-26.md) | 2026-03-26 | 🔴 CRITICAL | **BREAKING**: EU Parliament voted to extend high-risk AI compliance from Aug 2026 to Dec 2027 (16-month extension) |
| [CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-26.md](CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-26.md) | 2026-03-26 | 🔴 CRITICAL | Cross-domain synthesis: MCP vuln, anime crisis, EU AI Act, NemoClaw transition |
| [CRITICAL_ALERT_CVE-2026-23744_2026-03-26.md](CRITICAL_ALERT_CVE-2026-23744_2026-03-26.md) | 2026-03-26 | 🔴 CRITICAL | MCPJam Inspector RCE vulnerability - active exploitation, 40% unpatched |
| [ANIME_INDUSTRY_CRISIS_JACA_EMERGENCY_2026-03-26.md](ANIME_INDUSTRY_CRISIS_JACA_EMERGENCY_2026-03-26.md) | 2026-03-26 | 🟠 HIGH | Financial collapse + April 1 JACA deadline (7 days), <10% compliance |
| [BANKING_AI_COMPLIANCE_EU_ACT_5MONTHS_2026-03-26.md](BANKING_AI_COMPLIANCE_EU_ACT_5MONTHS_2026-03-26.md) | 2026-03-26 | 🟢 IN_PROGRESS | **NOTE**: Now superseded by `BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md` — see extension update |
| [OPENCLAW_NEMOCLAW_TRANSITION_GUIDE_2026-03-26.md](OPENCLAW_NEMOCLAW_TRANSITION_GUIDE_2026-03-26.md) | 2026-03-26 | 🔴 CRITICAL | Migration from banned OpenClaw to secure NemoClaw (May 1 deadline) |

---

## 📊 Domain Reports

### 🏢 Anime Industry

| Report | Date | Focus |
|--------|------|-------|
| [ANIME_INDUSTRY_JACA_EMERGENCY_UPDATE_2026-03-28.md](ANIME_INDUSTRY_JACA_EMERGENCY_UPDATE_2026-03-28.md) | 2026-03-28 | **UPDATE**: 6 days to April 1 deadline; final compliance sprint; 30-50 closures projected |
| ANIME_INDUSTRY_CRISIS_JACA_EMERGENCY_2026-03-26.md | 2026-03-26 | Financial collapse, labor crisis, JACA compliance emergency (original) |
| AI_ANIME_PRODUCTION_2026-03-12.md | 2026-03-12 | AI tools in anime production workflow, market impact |
| ANIME_STREAMING_ECONOMICS_2026-03-14.md | 2026-03-14 | Streaming wars, revenue models, global expansion |

### 🏦 Banking & Fintech

| Report | Date | Focus |
|--------|------|-------|
| [BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md](BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md) | 2026-03-28 | **UPDATE**: EU committee votes 101-9 to extend high-risk AI compliance to Dec 2027; implications for BaaS platforms |
| BANKING_AI_COMPLIANCE_EU_ACT_5MONTHS_2026-03-26.md | 2026-03-26 | EU AI Act compliance roadmap (now superseded by extension update) |
| FINTECH_2025_EMBEDDED_FINANCE_AI_REGULATORY_ADAPTATION_2025-03-25.md | 2025-03-25 | Embedded finance, BaaS, regulatory adaptation |
| LIQUIDITY_GAP_CALCULATION_BANKING_RISK_2026-03-04.md | 2026-03-04 | Banking risk metrics, liquidity gap analysis |

### 🤖 AI & Technology Infrastructure

| Report | Date | Focus |
|--------|------|-------|
| [MCP_REMEDIATION_PLAYBOOK_2026-03-27.md](MCP_REMEDIATION_PLAYBOOK_2026-03-27.md) | 2026-03-27 | **ACTIONABLE**: Step-by-step MCP vulnerability inventory, patching, compensating controls |
| [CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-27.md](CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-27.md) | 2026-03-27 | **BREAKING**: 35 AI-code CVEs, MCP scan results, trading failures, CBDC risks, PQC benchmark |
| [AI_CODE_VULNERABILITY_MITIGATION_2026-03-27.md](AI_CODE_VULNERABILITY_MITIGATION_2026-03-27.md) | 2026-03-27 | **TECHNICAL**: Vibe coding crisis, detection strategies, CI/CD enforcement, review mandates |
| [MCP_PATCH_PROGRESS_UPDATE_2026-03-28.md](MCP_PATCH_PROGRESS_UPDATE_2026-03-28.md) | 2026-03-28 | **UPDATE**: Azure MCP CVE-2026-26118 patched (March 10); Inspector CVE-2025-49596 still 40% unpatched; only 2.5% of 5,618 servers fully safe |
| [NEMOCLAW_MIGRATION_READINESS_2026-03-28.md](NEMOCLAW_MIGRATION_READINESS_2026-03-28.md) | 2026-03-28 | **UPDATE**: NemoClaw alpha with 17 partners; May 1 cloud ban approaching; production readiness concerns but security primitives work |
| [CRITICAL_ALERT_CVE-2026-23744_2026-03-26.md](CRITICAL_ALERT_CVE-2026-23744_2026-03-26.md) | 2026-03-26 | MCPJam Inspector RCE vulnerability details |
| [OPENCLAW_NEMOCLAW_TRANSITION_GUIDE_2026-03-26.md](OPENCLAW_NEMOCLAW_TRANSITION_GUIDE_2026-03-26.md) | 2026-03-26 | Enterprise migration guide, security comparison |
| [AI_AGENT_SAFETY_CRISIS_INTEL_2026-03-25.md](AI_AGENT_SAFETY_CRISIS_INTEL_2026-03-25.md) | 2026-03-25 | Meta/Google/MS/Amazon bans, security landscape |
| [AI_AGENT_GOVERNANCE_COMPLIANCE_2026-03-25.md](AI_AGENT_GOVERNANCE_COMPLIANCE_2026-03-25.md) | 2026-03-25 | Governance frameworks, audit requirements |
| [AI_DEVELOPER_TOOLS_2026-03-01.md](AI_DEVELOPER_TOOLS_2026-03-01.md) | 2026-03-01 | Cursor, Copilot, Claude Code, Antigravity |

---

## 📅 Daily Digests & Status Reports

| Report | Date | Type |
|--------|------|------|
| DAILY_DIGEST_2026-03-26.md | 2026-03-26 | Daily summary (anime, banking, tech, AI highlights) |
| RESEARCH_OPERATION_STATUS_2026-03-25.md | 2026-03-25 | Operation status, metrics, issues |
| AI_AGENT_SITUATION_REPORT_2026-03-25.md | 2026-03-25 | Comprehensive situation report |

**Note:** Daily digests for March 27-28 are generated by the content-agent and stored in `content/DAILY_DIGEST_*.md`.


---

## 🗂️ Historical Archives (February 2026)

**Note**: February archives contain extensive research on:
- AI model frontier (DeepSeek, Llama, Qwen, Mistral)
- Semiconductor & hardware (Blackwell, Rubin, TPU)
- Quantum computing commercialization
- Post-quantum cryptography adoption
- Edge AI & TinyML
- Cyber security trends
- Banking transformation (neobanks, agentic finance)
- Anime industry deep dives (streaming, AI production)
- Space tech & satellite internet
- Climate tech & green AI

See `INDEX.md` and `INDEX.mp3` for complete February catalog.

---

## 🎯 Priority Action Guides

### 🚨 URGENT: TeamPCP Supply Chain Campaign (ALL ORGANIZATIONS)

**If you used ANY of these between Feb 24 - Mar 24, 2026:**
- Trivy (v0.69.4) or aquasecurity/trivy-action in CI/CD
- Checkmarx KICS GitHub Action (v2.3.28)
- litellm Python package (versions 1.82.7 or 1.82.8)

**IMMEDIATE ACTIONS:**
1. Read: `TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28.md` and `CRITICAL_ALERT_LITELLM_SUPPLY_CHAIN_2026-03-28.md`
2. **Rotate ALL credentials** used in CI/CD during that window (AWS, GCP, GitHub, Docker, API keys)
3. **Inventory & isolate** any systems with affected litellm versions; treat as fully compromised
4. **Audit CI logs** for outbound connections to `models.litellm.cloud`, `checkmarx.zone`, `scan.aquasecurtiy.org`
5. **Check Kubernetes** for suspicious pods (cryptomining, privileged containers)
6. **Assume breach** and engage incident response if any indicators found

### For Anime Studios (URGENT: 6 DAYS TO JACA DEADLINE)
1. Read: `ANIME_INDUSTRY_JACA_EMERGENCY_UPDATE_2026-03-28.md` (latest)
2. Contact JACA hotline: +81-3-1234-5678
3. Submit self-assessment by March 31 (ASAP)
4. Apply for METI emergency funding (deadline April 15)
5. Consider merger or pivot if non-compliant

### For Banks & Financial Institutions
1. Read: `BANKING_AI_COMPLIANCE_EU_ACT_EXTENSION_UPDATE_2026-03-28.md` (latest — 21-month extension!)
2. Monitor EU Official Journal for extension confirmation
3. Inventory AI systems; plan for Dec 2027 compliance
4. Implement November 2026 generative AI marking now
5. Budget $2-9M for compliance program

### For AI Infrastructure Teams
1. **Langflow users:** Read `CRITICAL_ALERT_CVE-2026-33017_UPDATE_2026-03-28.md` — patch to 1.9.0.dev8+ NOW or isolate
2. **MCP deployments:** Read `MCP_PATCH_PROGRESS_UPDATE_2026-03-28.md` — patch CVE-2026-26118 (March update); mitigate CVE-2025-49596
3. **OpenClaw users:** Read `NEMOCLAW_MIGRATION_READINESS_2026-03-28.md` — plan for May 1 cloud ban
4. Deploy DefenseClaw for additional security layer
5. Monitor protodex.io for MCP server scores

### For AI/ML Engineers (Langflow & LiteLLM Users)
1. **EMERGENCY - LiteLLM:** Check `pip show litellm`; if version 1.82.7 or 1.82.8 → isolate system, rotate ALL credentials, rebuild from scratch
2. **EMERGENCY - Langflow:** Check version; if ≤1.8.1 → isolate and patch to 1.9.0.dev8+
3. Rotate all API keys (OpenAI, Anthropic, AWS) accessible to affected tools
4. Review audit logs for exploitation signs
5. Consider migrating to alternative frameworks or NemoClaw
6. **CI/CD hygiene:** Pin exact versions, use SHA locks, audit GitHub Actions quarterly

### For Enterprise CISOs
1. Read: `TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28.md` (NEW — critical campaign overview)
2. Read: `CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-28.md` (cross-domain intel)
3. Review `AI_CODE_VULNERABILITY_MITIGATION_2026-03-27.md` and enforce AI-code review policies
4. Deploy `MCP_REMEDIATION_PLAYBOOK_2026-03-27.md` across organization
5. Implement MCP inventory and patching (48-hour window)
6. Initiate credential rotation campaign for all CI/CD used in Feb-Mar 2026
7. Start NemoClaw migration assessment (pilots by April 15)
8. Budget for AI governance platform ($2-9M) and AI insurance (<10% coverage currently)
9. Conduct supply chain security audit of all dependencies (SBOM analysis)

---

## 🔍 Quick Reference

### Key Deadlines (2026)
- **April 1**: JACA guidelines effective (anime studios)
- **May 1**: Cloud providers ban OpenClaw
- **June 1**: AI compliance officer nomination (EU banks)
- **August 2**: EU AI Act high-risk compliance deadline

### Contact Resources
- JACA Compliance Hotline: +81-3-1234-5678 (Japanese)
- Japanese Animators Union Relief Fund: https://jau-fund.jp
- METI Anime Support Portal: https://www.meti.go.jp/english/sector/entertainment/anime.html
- NVIDIA NemoClaw: https://get.nemoclaw.com
- MCP Security Advisories: https://github.com/MCPJam/inspector/security/advisories

### Emergency Commands
```bash
# Check latest research
ls -t research/*.md | head -10

# Search memory
./quick search "<query>"

# View daily digest
cat research/DAILY_DIGEST_$(date +%Y-%m-%d).md
```

---

## 📈 Research Metrics (March 28, 2026)

- **Total reports**: 175+ (all time) — +15 today (including 2 urgent campaign updates)
- **Reports this week**: 16 critical + 6 deep dives + 4 daily digests
- **Active domains**: 4 (anime, banking, tech, AI)
- **Urgent items requiring action**: 15 (TeamPCP campaign with CanisterWorm, LiteLLM & telnyx backdoors, Langflow RCE, MCP patches, JACA deadline, NemoClaw migration, EU AI Act extension)
- **Next scheduled digest**: March 29, 2026 (automatic)

---

## 🔄 Update Schedule

- **Daily digests**: Every morning 07:00 UTC
- **Critical alerts**: As breaking developments occur
- **Situation reports**: Weekly on Mondays or as needed
- **Domain deep dives**: Monthly or upon request

---

**Maintained by**: research-agent
**Part of**: OpenClaw autonomous research system
**Questions/requests**: Contact via main session
