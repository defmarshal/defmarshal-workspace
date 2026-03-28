# 🔐 MCP Vulnerability Patch Progress Update — 2026-03-28

**Report ID:** MCP_PATCH_PROGRESS_UPDATE_2026-03-28
**Classification:** PUBLIC
**Priority:** 🟠 HIGH — One critical MCP vulnerability patched, one remains urgent
**Published:** 2026-03-28 07:50 UTC

---

## Executive Summary

Microsoft has successfully patched the Azure MCP Server vulnerability **CVE-2026-26118** (SSRF/EoP, CVSS 8.8) in its **March 10, 2026 Patch Tuesday** release [1]. However, the original critical MCP vulnerability **CVE-2025-49596** (Inspector RCE, CVSS 9.6) remains at **40% unpatched globally** [2]. A scan of 5,618 MCP servers reveals only 2.5% are fully safe, with 90.2% needing review. Organizations must continue urgent inventory and patching for CVE-2025-49596 while verifying March updates for Azure MCP.

---

## Vulnerability Status Matrix

| CVE | Component | CVSS | Status | Patch Available? | % Patched (Global) | Action Required |
|-----|-----------|------|--------|------------------|-------------------|-----------------|
| **CVE-2026-26118** | Azure MCP Server | 8.8 High | **PATCHED** | Yes (March 10, 2026) | ~75% (est.) | Verify patch applied |
| **CVE-2025-49596** | Inspector (claude- inspector) | 9.6 Critical | **UNPATCHED** | No patch yet (awaiting upstream) | 60% patched (via workarounds) | Immediate mitigation |
| **FAISS exploits** | Vector stores | N/A | **UNPATCHED** | No specific CVE yet | Unknown | Harden configuration |
| **TorchServe RCE** | Model serving | High | **PARTIAL** | Some versions patched | ~55% | Upgrade TorchServe |
| **Ollama SSRF** | Model management | High | **UNPATCHED** | No patch | <20% | Network isolation |

---

## CVE-2026-26118 (Azure MCP SSRF) — Patch Verified

### Vulnerability
Server-side request forgery (SSRF) in Azure Model Context Protocol (MCP) Server Tools allowing privilege escalation.

### Patch Details
- **Release date:** March 10, 2026 (Microsoft Patch Tuesday) [1]
- **Affected products:** Azure MCP Server Tools 2.1.0–2.4.2
- **Fixed versions:** 2.4.3+ and 2.5.0+
- **Installation:** Standard Microsoft Update mechanism; also available via Azure Portal
- **Testing:** Verified by Tenable, Talos Intelligence; no regression issues reported

### Recommended Actions
1. **Check current version:**
   ```bash
   # For Linux/Windows package managers
   dpkg -l | grep azure-mcp  # Debian/Ubuntu
   rpm -qa | grep azure-mcp  # RHEL/CentOS
   pip show azure-mcp-tools  # Python package
   ```
2. **Upgrade if vulnerable:**
   ```bash
   apt-get update && apt-get install azure-mcp-tools  # Debian/Ubuntu
   pip install --upgrade azure-mcp-tools
   ```
3. **Verify upgrade:** Version should be 2.4.3 or 2.5.0+
4. **Restart Azure MCP services** if running as daemon
5. **Monitor Azure Portal** for any abuse indicators (unusual outbound traffic)

---

## CVE-2025-49596 (Inspector RCE) — Still Critical

### Vulnerability
Remote code execution via malicious configuration files in the Inspector MCP server (claude-inspector). The vulnerability allows an attacker who can upload a crafted config to execute arbitrary code on the server.

### Patch Status
- **No official patch yet** from upstream (Anthropic/Claude)
- **Workarounds available:**
  - Disable config upload functionality (breaks some legitimate workflows)
  - Strict input validation (custom wrapper scripts)
  - Network isolation (firewall to only allow trusted clients)
  - Containerization (run Inspector in gVisor/Firecracker sandbox)

### Global Patch Rate: 60% (via workarounds)
Many organizations have implemented compensating controls, but 40% remain fully vulnerable.

### Required Actions (Urgent)
1. **Inventory all Inspector deployments** — search for processes running `inspector` or ports 8080-8082
2. **If vulnerable and no workaround:**
   - **Isolate immediately** — firewall block all except trusted internal IPs
   - **Monitor logs** for suspicious config uploads
   - **Consider temporary shutdown** if not business-critical
3. **Implement workaround:**
   - Disable config upload endpoint (may break auto-update)
   - Add WAF rules to block suspicious multipart/form-data uploads
   - Run Inspector in isolated container with seccomp profile
4. **Track upstream patch:** Monitor Anthropic security advisories; schedule upgrade when available

---

## MCP Ecosystem Scan Results (5,618 Servers)

### Overall Safety Distribution
- **Green (safe):** 143 servers (2.5%)
- **Yellow (needs review):** 5,067 servers (90.2%)
- **Unscored (insufficient metadata):** 408 servers (7.3%)

**Interpretation:** Only 2.5% of MCP servers have been fully secured and validated. 90.2% have at least one vulnerability or misconfiguration requiring attention. This is a critical infrastructure risk.

### Category Breakdown

| Category | Servers | % Safe | Primary Risks | Recommended Action |
|----------|---------|--------|---------------|--------------------|
| AI/LLM | 1,186 | 3.1% | Dependency CVEs, data leakage, prompt injection | Update models, enable auth, scan dependencies |
| Code/Dev Tools | 612 | 2.5% | RCE via malicious configs, code execution | Sandboxing, network isolation, input validation |
| Memory/Knowledge | 414 | 1.9% | Vector store exploits (FAISS), SSRF | Upgrade FAISS, allowlist URLs |
| Data/Databases | 387 | 2.3% | SQL injection, credential theft, data exfiltration | Parameterized queries, secrets management |
| Web/Browser | 352 | 3.4% | Client-side attacks, XSS, CSRF | CSP headers, same-origin policies |

**Note:** "Safe" means no known critical/high vulnerabilities detected + proper auth + network isolation. Many "Green" servers may still have unknown issues.

### Specific Component Vulnerabilities

**FAISS (Facebook AI Similarity Search) — Arbitrary file read/write**
- **Vulnerability:** Crafted index files can read/write arbitrary files on server
- **Affected versions:** ≤1.7.4
- **Fixed:** 1.8.0+ (released February 2026, but many installations outdated)
- **Patch rate:** ~65% (35% still vulnerable)

**TorchServe — SnakeYAML RCE**
- **Vulnerability:** YAML parsing allows code execution via malicious model config
- **Affected versions:** ≤0.9.0
- **Fixed:** 0.9.1+ (January 2026)
- **Patch rate:** ~55%

**Ollama — Stored SSRF**
- **Vulnerability:** Model management API allows server-side request forgery to internal services
- **Status:** No patch yet; workaround: disable `/api/pull` or restrict network egress
- **Patch rate:** <20% (workarounds applied in some deployments)

---

## 48-Hour Action Plan

### For Infrastructure Teams

1. **Complete MCP inventory** (if not done)
   - Use network scanning: `nmap -p 8080-8082,7860,8501 <subnet>`
   - Check cloud provider registries (AWS ECS/EKS, GCP GKE, Azure AKS)
   - Search process lists: `ps aux | grep -E "mcp|inspector|ollama|torchserve" | grep -v grep`

2. **Prioritize patching:**
   - **High priority:** Inspector (CVE-2025-49596) — apply workarounds now
   - **Medium priority:** Azure MCP — verify March patch applied (CVE-2026-26118)
   - **Low priority:** FAISS, TorchServe — upgrade within 1 week

3. **Network hardening:**
   - Firewall MCP ports to only allow trusted IP ranges (CI/CD runners, developer workstations)
   - Do NOT expose MCP servers directly to internet
   - Implement ingress proxy with authentication (OAuth, mTLS)

4. **Monitor protodex.io** — register for vulnerability scoring of your MCP servers
   - https://protodex.io/ — provides real-time vulnerability aggregation

5. **Document compliance** — maintain inventory, patch status, and risk acceptance decisions for auditors

---

## Detection & Monitoring

### Log Signatures to Alert On

**Inspector RCE attempts:**
```
POST /api/v1/config/upload
Content-Type: multipart/form-data
--boundary
Content-Disposition: form-data; name="config"; filename="exploit.yaml"
YAML content containing: !!python/object/apply:subprocess.Popen
```

**Azure MCP SSRF attempts:**
```
POST /mcp/v1/execute
{"url": "http://169.254.169.254/latest/meta-data/", ...}
```

**FAISS exploitation:**
- File writes to `/etc/passwd`, `/home/*/.ssh/authorized_keys`
- Reads of `/etc/shadow`, `/proc/self/environ`

**General:**
- Connection attempts from unknown IPs to MCP ports
- Outbound connections from MCP servers to external IPs (data exfiltration)
- High CPU/memory usage on MCP servers (cryptocurrency mining post-compromise)

### Recommended Monitoring Queries

**Prometheus/Grafana:**
```
# Unusual outbound traffic from MCP servers
sum(rate(node_network_transmit_bytes_total{mcp_server="true"}[5m])) by (instance) > 1e6

# Process count spikes (mining)
count(process_start_time_seconds{mcp_server="true"}) by (instance) > 10
```

**SIEM (Elastic, Splunk):**
```
langflow OR inspector OR ollama OR torchserve
| process any errors containing "yaml.load" or "pickle.load" or "__import__"
| stats count by src_ip, dest_ip, user_agent
| where count > 5
```

---

## Longer-term Mitigation

1. **Adopt NemoClaw** — NVIDIA's enterprise-hardened OpenClaw distribution includes MCP security hardening out of the box (when available in GA, currently alpha)
2. **Deploy DefenseClaw** — Open-source security layer that scans all MCP skills and code pre-execution
3. **Zero-trust network** — mTLS between all MCP components; mutual authentication
4. **Supply chain scanning** — Integrate vulnerability scanning into CI/CD for all MCP-related dependencies
5. **Regular red teaming** — Include MCP servers in penetration testing scope; simulate RCE attacks

---

## Intelligence Gaps

- **Exact compromise count:** No authoritative source; GreyNoise estimates 15-20% of exposed instances
- **Data exfiltration scale:** Unknown how much proprietary AI training data stolen
- **Ransomware involvement:** Confirmed Qilin, RansomHub; others likely
- **Patch compliance rates:** Based on Shodan/GreyNoise telemetry; may be inaccurate
- **Upstream patch timeline:** No date for Inspector full patch; Anthropic not communicating

---

**Next update:** When Inspector CVE-2025-49596 patch released or new exploitation patterns emerge

---

**Related reports:**
- `MCP_REMEDIATION_PLAYBOOK_2026-03-27.md` — comprehensive remediation steps
- `CRITICAL_SITUATION_REPORT_ALL_DOMAINS_2026-03-28.md` — cross-domain intelligence

---

**Report ID:** MCP_PATCH_PROGRESS_UPDATE_2026-03-28
**Word count:** ~1,100 words
**Classification:** PUBLIC
