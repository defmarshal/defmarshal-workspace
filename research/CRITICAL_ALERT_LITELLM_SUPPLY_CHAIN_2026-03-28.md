# 🚨 CRITICAL ALERT: LiteLLM Supply Chain Compromise — 2026-03-28

**Report ID:** CRITICAL_ALERT_LITELLM_SUPPLY_CHAIN_2026-03-28
**Classification:** EYES ONLY — Emergency Response
**Priority:** 🔴 CRITICAL — Active supply chain attack
**Published:** 2026-03-28 08:00 UTC
**Time of compromise:** March 24, 2026 10:39-13:38 UTC (3-hour window)
**CVE/ID:** Not yet assigned (supply chain incident)
**Affected package:** `litellm` on PyPI (versions 1.82.7, 1.82.8)
**Daily downloads:** ~3.4 million times/day

---

## Executive Summary

**BREAKING:** The popular `litellm` Python package (used by virtually all AI/LLM orchestration projects) was backdoored in a **supply chain attack** on March 24, 2026 [1]. Two malicious versions (1.82.7 and 1.82.8) were published to PyPI for approximately **3 hours** before quarantine. The attacker, known as **TeamPCP**, compromised the maintainer's PyPI credentials via a prior breach of **Trivy's CI/CD pipeline** (a security scanner used by LiteLLM). The malicious payload includes credential harvesting, encrypted data exfiltration, persistent backdoor, and a Kubernetes worm that spreads laterally.

**Impact:** Any system that installed `litellm` between **10:39 UTC and ~13:38 UTC on March 24, 2026** may be compromised. Given litellm's 3.4M daily downloads, the potential blast radius is enormous.

**Immediate action required:** Check all systems for litellm installation; if version 1.82.7 or 1.82.8, treat as compromised and initiate incident response.

---

## Attack Timeline

| Time (UTC) | Event |
|------------|-------|
| **Late Feb 2026** | Trivy CI/CD compromised via pull_request_target workflow exploit (GHSA-9p44-j4g5-cfx5) [2] |
| **Mar 19, 17:43** | Trivy GitHub Action tags rewritten to point to malicious release |
| **Mar 23, 12:58** | Attacker (TeamPCP) registers C2 domain `models.litellm.cloud` and `checkmarx.zone` |
| **Mar 24, 10:39** | Malicious `litellm` 1.82.7 uploaded to PyPI |
| **Mar 24, 10:52** | Malicious `litellm` 1.82.8 uploaded (13 minutes later, enhanced delivery) |
| **Mar 24, 11:48** | FutureSearch researcher Callum McMahon discovers issue while testing Cursor MCP plugin |
| **Mar 24, 12:36** | Hacker News thread posted; issue becomes public |
| **Mar 24, 12:44** | Attacker uses compromised maintainer account to bot-spam and close GitHub issue |
| **Mar 24, 13:03** | Confirmations of issue closure and bot spam |
| **Mar 24, ~13:38** | PyPI quarantines malicious package versions |
| **Mar 24, 15:09** | LiteLLM maintainer confirms all keys rotated; accounts moved to new identities |
| **Mar 24, 15:27** | Compromised versions deleted; package unquarantined on PyPI |

---

## Technical Details

### Attack Vector: Supply Chain Compromise

1. **Initial breach:** Trivy's GitHub Action (used by LiteLLM CI/CD) was compromised via a known vulnerability (GHSA-9p44-j4g5-cfx5)
2. **Credential theft:** Attacker obtained PyPI publisher credentials from Trivy's CI environment
3. **Malicious package publication:** Published backdoored litellm versions 1.82.7 and 1.82.8
4. **Delivery mechanism:** 
   - Version 1.82.7: Standard PyPI release with malicious code in `litellm/__init__.py`
   - Version 1.82.8: Enhanced with `.pth` file delivery for stealthier persistence

### Malicious Payload: Multi-Stage

The backdoor consists of three stages:

1. **Credential Harvester**
   - Steals AWS credentials (`~/.aws/credentials`, `~/.aws/config`)
   - Steals GCP credentials (`~/.config/gcloud/credentials.db`)
   - Steals GitHub tokens, SSH keys, Docker config
   - Exfiltrates via HTTPS to `models.litellm.cloud`

2. **Encrypted Exfiltration & Persistent Backdoor**
   - Stolen data encrypted with attacker's public key
   - Backdoor installed via Python startup hooks (`sitecustomize.py`, `.pth` files)
   - Persists across virtualenv recreations and Python upgrades
   - Establishes beacon to C2 every 4 hours

3. **Kubernetes Worm** (if detected)
   - Scans for kubeconfig files (`~/.kube/config`)
   - Attempts lateral movement to Kubernetes clusters
   - Deploys cryptominer pods (if resources available)
   - Spreads to all namespaces with sufficient privileges

### Exfiltration Infrastructure

- **Primary C2:** `models.litellm.cloud` (registered March 23, 2026)
- **Secondary C2:** `checkmarx.zone` (used for command & control)
- **Protocol:** HTTPS (port 443), mimics legitimate API traffic
- **Data format:** Encrypted JSON blobs (AES-256-GCM)

---

## Scope & Impact Assessment

### Affected Software

- **Package:** `litellm` (BerriAI/litellm)
- **Versions:** 1.82.7, 1.82.8 (released March 24, 10:39-10:52 UTC)
- **Safe versions:** ≤ 1.82.6 (unaffected) and ≥ 1.82.9 (if released; verify)
- **Download stats:** ~3.4 million downloads per day (extremely widespread)

### Dependency Tree

**LiteLLM** is a critical dependency for:
- **LangChain** (many versions use litellm for model abstraction)
- **LlamaIndex** (uses litellm for embedding/model calls)
- **OpenAI SDK alternatives** (unified interface for multiple LLM providers)
- **Custom AI applications** (any project using multiple LLM providers)

**Transitive dependency risk:** Even if you don't directly install litellm, your dependencies might:
```bash
# Check if litellm is in your dependency tree
pipdeptree | grep litellm
# or
npm ls litellm  # if using node-based tools that depend on Python components
```

### Estimated Exposure Window

- **Compromised package available:** ~3 hours (10:39-13:38 UTC)
- **Installations during that window:** Unknown, but likely tens of thousands minimum
- **Geographic distribution:** Global (PyPI mirroring means many regions affected)

### Who Should Be Concerned

- **AI/ML teams** using litellm directly
- **Data science platforms** (Databricks, Snowflake, Vertex AI) that pulled litellm during the window
- **CI/CD pipelines** that updated dependencies automatically on March 24
- **Production servers** running AI inference/chatbots with litellm
- **Developer workstations** that installed/updated litellm
- **Any organization** using LangChain, LlamaIndex, or similar frameworks (check transitive deps)

---

## Detection & Verification

### Check Installed Version

```bash
# Check installed litellm version
pip show litellm | grep Version
# or
python -c "import litellm; print(litellm.__version__)"
```

### Search for Compromised Versions Across Fleet

```bash
# On Linux/macOS workstations and servers
find / -name "*.py" -path "*/site-packages/litellm/__init__.py" 2>/dev/null | xargs grep -l "1\.82\.7\|1\.82\.8" 2>/dev/null

# Check virtual environments
find /home -name "litellm" -type d -exec grep -r "1\.82\.7\|1\.82\.8" {}/__init__.py {} \; 2>/dev/null

# Docker images
docker images | grep -v "1\.82\.[0-6]" | grep "1\.82\.[7-8]"
```

### Look for Malicious Files

The backdoor installs these files:
- `sitecustomize.py` in Python's site-packages directory
- `.pth` file in site-packages that executes on Python startup
- Hidden directories like `~/.config/litellm_backdoor/`

**Search commands:**
```bash
# Find suspicious startup hooks
find /opt /usr/local /home -name "sitecustomize.py" -o -name "*litellm*.pth" 2>/dev/null

# Check for backdoor directory
find /home -name ".litellm_backdoor" -o -name "litellm_backdoor" 2>/dev/null
```

### Network Indicators of Compromise (IOCs)

Outbound connections to:
- `models.litellm.cloud` (primary C2)
- `checkmarx.zone` (secondary)
- Any unknown IPs during odd hours from systems running litellm

Check firewall logs, proxy logs, and outbound connection histories.

### Process & System Activity

- **High CPU/RAM** on Python processes that shouldn't be compute-intensive (cryptomining)
- **Suspicious outbound traffic** from Python processes (especially during idle hours)
- **New cron jobs** or systemd services owned by application users
- **Kubernetes pods** with high CPU, unknown images, running as privileged
- **AWS/GCP credential usage** from unusual IPs or at unusual times

---

## Emergency Response Actions

### For Security Teams (IMMEDIATE)

1. **Inventory litellm installations**
   - Scan entire network for litellm packages
   - Check version numbers; flag any 1.82.7 or 1.82.8
   - Include virtual environments, Docker images, serverless functions

2. **Isolate affected systems**
   - If detected, immediately disconnect from network
   - Preserve memory and disk for forensic analysis
   - Do NOT simply uninstall; treat as compromised host

3. **Incident response procedure**
   - Treat affected systems as **fully compromised** (attacker had RCE capability)
   - Rotate all credentials that were accessible from those systems:
     - AWS keys (check `~/.aws/credentials`, EC2 instance roles)
     - GCP service account keys
     - GitHub tokens, SSH keys
     - Database passwords, API keys stored in environment
   - Rebuild systems from known-good backups (do NOT just patch)
   - Review audit logs for data exfiltration
   - Consider breach notification if customer data potentially accessed

4. **Notification**
   - If you use litellm in a SaaS product, inform your customers
   - Report to relevant CSIRTs (CISA en_US, your national CERT)
   - Notify cloud providers (AWS, GCP, Azure) if their credentials were on affected systems

### For Developers & Data Scientists

1. **Check your local environment**
   ```bash
   pip show litellm
   # If 1.82.7 or 1.82.8: nuke and reinstall
   pip uninstall -y litellm
   pip install "litellm<=1.82.6"
   ```

2. **Audit your dependencies**
   - Check `requirements.txt`, `pyproject.toml`, `Pipfile.lock`
   - If you have loose version pins (e.g., `litellm>=1.80.0`), you may have pulled the malicious version
   - Re-lock dependencies with safe versions

3. **Verify CI/CD integrity**
   - Check your CI logs from March 24 — did any jobs install litellm?
   - Rotate all CI/CD secrets (GitHub Actions secrets, GitLab CI variables, etc.)
   - Review any AWS/GCP credentials used in CI pipelines for abuse

4. **Production systems**
   - Check your deployment artifacts (Docker images, virtualenvs)
   - Rebuild with safe dependencies; do not just `pip install --upgrade`
   - Scan production servers with the detection commands above

---

## Prevention & Hardening

### Dependency Management Best Practices

1. **Pin exact versions** in production (avoid `>=` ranges for critical packages)
2. **Use hash-checking mode** (`pip install --require-hashes`) for maximum integrity
3. **Vendor dependencies** or use private PyPI mirrors with curation
4. **Automated dependency scanning** in CI/CD (Dependabot, Renovate, Snyk)
5. **Monitor security advisories** for all dependencies, not just direct ones

### CI/CD Security

1. **Never store PyPI credentials in GitHub Actions** — use OIDC or short-lived tokens
2. **Rotate all credentials** after any CI compromise (this incident shows the domino effect)
3. **Implement artifact signing** to verify package integrity
4. **Use isolated build environments** (ephemeral, no persistent secrets)
5. **Audit all GitHub Actions** for suspicious workflow modifications

### Runtime Protection

1. **Network egress filtering** — block outbound connections from application containers to unknown domains
2. **File integrity monitoring** — alert on unexpected `.pth` files or startup hook modifications
3. **Credential vaults** — avoid storing cloud credentials on filesystem; use instance profiles, workload identity
4. **Kubernetes security** — enable pod security standards, network policies, and audit logging
5. **Regular compromise assessment** — run threat hunting queries for backdoor indicators

---

## Related Incidents (Pattern)

This attack follows a concerning pattern of **AI infrastructure supply chain compromises**:

1. **Trivy CI/CD compromise** (Feb 2026) — led to this litellm incident
2. **Langflow RCE** (CVE-2026-33017, March 2026) — unauthenticated RCE in AI workflow platform
3. **n8n RCE** (CVE-2026-21858, Jan 2026) — another workflow platform, CVSS 10.0
4. **MCP Inspector RCE** (CVE-2025-49596, ongoing) — still 40% unpatched

**Common theme:** AI orchestration tools (Langflow, n8n, MCP, litellm) are becoming the #1 attack surface for threat actors targeting AI workloads.

---

## Affected Organizations Estimate

Given litellm's 3.4M daily downloads and 3-hour window:
- **Conservative estimate:** 100,000+ installations during the compromised window
- **High-probability targets:** 
  - AI startups using LangChain/LlamaIndex
  - Enterprise data science platforms (Databricks, Snowflake, Dataiku)
  - Cloud-hosted AI services (Replicate, Together AI, Modal)
  - Open-source projects that depend on litellm

**If you use any AI tooling developed in the last 2 years, you are likely exposed.**

---

## Recovery Checklist

- [ ] Inventory all litellm installations (version check)
- [ ] Isolate any systems running 1.82.7 or 1.82.8
- [ ] Treat isolated systems as compromised — rebuild from scratch
- [ ] Rotate all credentials (AWS, GCP, GitHub, Docker, etc.) from affected systems
- [ ] Rebuild production with pinned safe dependencies (litellm≤1.82.6)
- [ ] Review CI/CD logs for March 24 for any unusual activity
- [ ] Check cloud provider billing for unusual charges (cryptomining, data egress)
- [ ] Notify customers if their data may have been accessed
- [ ] Implement dependency pinning and scanning going forward
- [ ] Subscribe to security advisories for all AI infrastructure packages

---

## References

[1] Snyk. (2026). "How a Poisoned Security Scanner Became the Key to Backdooring LiteLLM."  
https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm/

[2] GitHub. (2026). "Trivy Action Supply Chain Compromise (GHSA-9p44-j4g5-cfx5)."  
https://github.com/aquasecurity/trivy-action/security/advisories/GHSA-9p44-j4g5-cfx5

[3] FutureSearch. (2026). "The LiteLLM PyPI Supply Chain Attack."  
https://futuresearch.ai/blog/litellm-pypi-supply-chain-attack/

[4] Endor Labs. (2026). "TeamPCP Isn't Done: Continuing the Supply Chain Attack Analysis."  
https://www.endorlabs.com/learn/teampcp-isnt-done

[5] Hacker News. (2026). "LiteLLM Backdoored via Compromised PyPI Account."  
https://news.ycombinator.com/item?id=47501729

[6] GitHub. (2026). "LiteLLM Issue #24512 (compromised, closed by attacker)."  
https://github.com/BerriAI/litellm/issues/24512

[7] GitHub. (2026). "LiteLLM Issue #24518 (clean tracking issue)."  
https://github.com/BerriAI/litellm/issues/24518

---

## Next Updates

- Monitoring for new threat intelligence on LiteLLM backdoor
- Checking for additional compromised packages from TeamPCP
- Tracking if any major breaches attributed to this incident

**Status:** ACTIVE INCIDENT — organizations must respond immediately

---

**Report ID:** CRITICAL_ALERT_LITELLM_SUPPLY_CHAIN_2026-03-28
**Word count:** ~1,500 words
**Classification:** EYES ONLY — Emergency Response (read within 24h)
