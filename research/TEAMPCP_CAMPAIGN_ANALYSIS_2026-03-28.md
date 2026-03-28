# 🛡️ TEAMPCP SUPPLY CHAIN CAMPAIGN: Comprehensive Threat Intelligence — 2026-03-28

**Report ID:** TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28
**Classification:** EYES ONLY — Security Operations
**Priority:** 🔴 CRITICAL — Active, expanding campaign
**Published:** 2026-03-28 08:15 UTC
**Last updated:** 2026-03-28 08:15 UTC
**Timeframe:** February 24 — present (ongoing)
**Threat actor:** TeamPCP (aliases: PCPcat, Persy_PCP, ShellForce, DeadCatx3)

---

## Executive Summary

A sophisticated threat actor known as **TeamPCP** is conducting an ongoing **multi-vector supply chain attack campaign** targeting the AI/cloud-native ecosystem [1][2][3]. The campaign began with a compromise of **Trivy's CI/CD pipeline** in late February 2026 and has expanded to include **Checkmarx KICS GitHub Actions** and the **LiteLLM PyPI package**. The attacker demonstrates advanced tradecraft: credential harvesting via malicious GitHub Actions, downstream package poisoning, and a credential stealer payload that targets AWS/GCP credentials, webhooks, and Kubernetes clusters.

**Current known impacts:**
- **Trivy**: 75+ malicious releases, thousands of affected CI pipelines
- **Checkmarx KICS**: Version 2.3.28 of GitHub Action compromised
- **LiteLLM**: Versions 1.82.7 and 1.82.8 backdoored (3.4M daily downloads)
- **Potential downstream**: Unknown number of dependent projects and downstream users

**Recommended immediate action:** Treat any CI/CD usage of Trivy (v0.69.4), Checkmarx KICS action (v2.3.28), or litellm (1.82.7-1.82.8) between late February and March 24, 2026 as compromised. Rotate all credentials, audit CI logs, and rebuild affected systems.

---

## Campaign Timeline

| Date (UTC) | Event | Vector |
|------------|-------|--------|
| **Late Feb 2026** | Trivy GitHub Action compromised via pull_request_target exploit (GHSA-9p44-j4g5-cfx5) | CI/CD Poisoning |
| **Feb 24 - Mar 19** | Attacker gathers intelligence, tests payloads, maps CI/CD ecosystem | Reconnaissance |
| **Mar 19, 17:43** | First malicious Trivy v0.69.4 release force-pushed; credential stealer deployed to affected CI pipelines | Supply Chain |
| **Mar 19-23** | Thousands of repositories unknowingly execute malicious GitHub Actions; credentials exfiltrated | Mass Compromise |
| **Mar 23, 12:58** | Attacker registers C2 domains: `checkmarx.zone`, `models.litellm.cloud` | Infrastructure |
| **Mar 24, 10:39** | Malicious litellm 1.82.7 uploaded to PyPI using stolen credentials | Package Poisoning |
| **Mar 24, 10:52** | Malicious litellm 1.82.8 uploaded (enhanced delivery) | Package Poisoning |
| **Mar 24, 11:48** | Callum McMahon (FutureSearch) discovers issue while testing Cursor MCP plugin | Discovery |
| **Mar 24, 12:36** | Public disclosure via Hacker News; GitHub issue opened | Public Alert |
| **Mar 24, 12:44** | Attacker uses compromised LiteLLM maintainer account to bot-spam and close GitHub issue | Cover-up |
| **Mar 24, ~13:38** | PyPI quarantines malicious litellm versions | Containment |
| **Mar 24, 15:09** | LiteLLM maintainer rotates all keys; accounts moved to new identities | Response |
| **Mar 24, 15:27** | Compromised versions deleted; package unquarantined | Recovery |
| **Mar 25-27** | Analysis from Sysdig, Microsoft, Arctic Wolf reveals Checkmarx KICS wave and campaign scope | Attribution |
| **Mar 28 (today)** | Ongoing: Organizations still discovering compromises; TeamPCP may still be active | Active Threat |

---

## Attack Vectors & Tradecraft

### Phase 1: CI/CD Compromise (Credential Harvesting)

**Target:** GitHub Actions workflows that use `aquasecurity/trivy-action` or `Checkmarx/ast-github-action`.

**Method:** 
- Exploited GHSA-9p44-j4g5-cfx5 — a vulnerability in Trivy's CI allowing pull_request_target code execution
- Force-pushed 75 of 76 tags in `aquasecurity/trivy-action` repo to point to malicious commits
- Same pattern observed in `Checkmarx/ast-github-action` v2.3.28 approximately 4 days later, suggesting stolen credentials were reused

**Payload:**
- Modified `entrypoint.sh` (Trivy) or `setup.sh` (Checkmarx) to include credential stealer
- Scanned `/proc/*/mem` for secrets in memory
- Queried cloud metadata services (AWS IMDS 169.254.169.254, GCP metadata)
- Searched workspace for Slack/Discord webhooks
- Exfiltrated aggregated secrets via HTTPS to C2 domains

### Phase 2: Downstream Package Poisoning

**Target:** PyPI packages with maintainers whose CI credentials were stolen.

**Method:**
- Used stolen PyPI credentials from compromised CI runs to publish malicious packages
- First observed: `litellm` 1.82.7 and 1.82.8
- Likely other packages may have been targeted (ongoing investigation)

**Payload Enhancements (litellm 1.82.8):**
- Added `.pth` file for stealthier persistence (executes on Python startup automatically)
- Three-stage backdoor: credential harvester → encrypted exfiltration → persistent backdoor + Kubernetes worm
- C2 domains: `models.litellm.cloud`, `checkmarx.zone`

---

## Indicators of Compromise (IOCs)

### Git/GitHub

- **Repository**: `aquasecurity/trivy-action` — malicious tags v0.69.4 and related versions
- **Repository**: `Checkmarx/ast-github-action` — version 2.3.28
- **GitHub accounts**: LiteLLM maintainer account compromised (Krish Dholakia) — defaced profiles, bot-spam
- **Commits**: Look for commits modifying `entrypoint.sh` or `setup.sh` that add curl commands to exfiltrate `tpcp.tar.gz`

### Network IOCs

**C2 domains:**
- `scan.aquasecurtiy[.]org` (typosquat of aquasecurity)
- `checkmarx[.]zone` (typosquat)
- `models.litellm[.]cloud`

**IP addresses:**
- `45.148.10.212` (scan.aquasecurtiy.org)
- Other IPs may be used; monitor for outbound connections from CI runners to suspicious domains during build time

### File IOCs

**In CI environments:**
- `/tmp/tmp.*/tpcp.tar.gz` — encrypted archive of stolen secrets
- Modified `entrypoint.sh` or `setup.sh` containing curl POST to C2 domains

**In Python environments (litellm backdoor):**
- `sitecustomize.py` in site-packages
- `.pth` file that executes on Python startup
- `~/.config/litellm_backdoor/` or similar hidden directories
- Modified `litellm/__init__.py` containing base64-encoded payloads

### Process IOCs

- CI runners executing `curl` to unknown domains with `tpcp.tar.gz` upload
- Python processes spawning unexpected outbound connections
- Kubernetes pods with cryptomining behavior (high CPU, unknown images)

---

## Affected Ecosystems

### 1. CI/CD Infrastructure

Any organization that used the following in their CI pipelines between late February and March 24, 2026:
- **Trivy** (v0.69.4, possibly other versions during the malicious window)
- **Checkmarx KICS** GitHub Action (v2.3.28)
- **Other GitHub Actions** that may have been compromised via stolen credentials (potential expansion)

**Impact:** CI secrets (cloud credentials, API keys, tokens) likely exfiltrated. Treat all secrets used in affected pipelines as compromised.

### 2. AI/ML Python Ecosystem

- **litellm** users (1.82.7, 1.82.8): ~3.4M daily downloads; backdoor provides full system access
- **LangChain**, **LlamaIndex**, and any framework that depends on litellm as a transitive dependency
- Projects that automatically update dependencies (Dependabot, Renovate) may have pulled malicious versions

**Impact:** Production servers, developer workstations, and data science platforms potentially backdoored.

### 3. Downstream Projects

Any project that:
- Uses Trivy for security scanning (thousands of repos)
- Uses Checkmarx KICS for AST
- Depends on litellm (directly or transitively)
- Runs CI on GitHub Actions that pulled compromised actions

**Potential blast radius:** Could be as wide as 100,000+ repositories and millions of end-user systems.

---

## Detection & Response Playbook

### Step 1: CI/CD Inventory & Analysis

```bash
# Search GitHub organization for compromised actions
# Use GitHub API or GitHub Search:
# - aquasecurity/trivy-action@v0.69.4
# - Checkmarx/ast-github-action@2.3.28

# Check git logs for suspicious commits
git log --oneline --grep="TeamPCP" --all
git log --oneline --since="2026-02-24" --until="2026-03-25" -- path/to/action

# Review GitHub Actions logs for outbound connections during builds
# Look for curl commands to unknown domains
```

### Step 2: Credential Rotation (Assume Compromise)

If you used Trivy or Checkmarx KICS in CI:
1. Rotate all AWS keys (including EC2 instance roles if they were active during the window)
2. Rotate GCP service account keys
3. Rotate GitHub tokens and SSH keys used in CI
4. Rotate Docker registry credentials
5. Rotate any third-party API keys (OpenAI, Anthropic, etc.) stored as CI secrets
6. Enable MFA on all accounts
7. Review audit logs for unusual API calls (new instances, data exports, etc.)

### Step 3: Litellm System Forensics

```bash
# Check installed version
pip show litellm | grep Version

# If 1.82.7 or 1.82.8:
# 1. Isolate host from network
# 2. Preserve memory and disk for forensic analysis
# 3. Do NOT just uninstall; treat as compromised
# 4. Rebuild from known-good backup after credential rotation

# Search for backdoor artifacts
find / -name "sitecustomize.py" 2>/dev/null | xargs grep -l "litellm" 2>/dev/null
find / -name "*.pth" 2>/dev/null | xargs grep -l "litellm" 2>/dev/null
find /home -name ".litellm_backdoor" -o -name "*litellm*backdoor*" 2>/dev/null
```

### Step 4: Kubernetes Worm Check

If litellm was installed on Kubernetes nodes:

```bash
# Check for suspicious pods
kubectl get pods --all-namespaces --field-selector=status.phase=Running | grep -i "xmr\|miner\|unknown"
kubectl describe pod <suspicious-pod> -n <namespace>

# Check for privileged pods
kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged==true)'

# Review audit logs for unexpected pod deployments
kubectl logs -n kube-system <audit-log-pod> | grep -i "teampecp\|litellm\|checkmarx"
```

### Step 5: Incident Response & Notification

1. **Treat as APT-level compromise** — TeamPCP demonstrates sophisticated tradecraft
2. **Engage forensic team** — preserve evidence, perform root cause analysis
3. **Customer notification** — if customer data potentially accessed, follow breach notification laws
4. **Report to CSIRTs** — CISA (en_US), your national CERT, cloud providers
5. **Consider cyber insurance claim** — supply chain attacks often covered

---

## Threat Actor Profile: TeamPCP

**Aliases:** PCPcat, Persy_PCP, ShellForce, DeadCatx3

**TTPs (MITRE ATT&CK):**
- T1546.018: Python startup hooks (persistence via `.pth` files)
- T1003: Credential dumping (scraping memory, cloud metadata)
- T1610: Deploy container (Kubernetes worm)
- T1190: Exploit public-facing application (CI/CD vulnerabilities)
- T1105: Ingress tool transfer (downloading additional payloads)
- T1082: System information discovery
- T1041: Exfiltration over C2 channels (HTTPS)

**Motivation:** Unknown — could be financial (cryptomining), espionage (credential theft), or hacktivism (disruption)

**Sophistication:** High — demonstrates deep understanding of CI/CD ecosystems, supply chain mechanics, and cloud credential harvesting

**Campaign pattern:** 
1. Compromise widely-used CI/CD tool (Trivy)
2. Steal CI secrets from thousands of repos
3. Use stolen credentials to poison downstream packages (litellm)
4. Expand to related tools (Checkmarx KICS)
5. **Likely more targets exist** — any project using Trivy/Checkmarx could have been a springboard

---

## Prevention & Long-term Hardening

### CI/CD Security Best Practices

1. **Never store long-lived credentials in GitHub Actions** — use OIDC or short-lived tokens
2. **Pin action versions** to immutable SHA256 hashes, not floating tags:
   ```yaml
   - uses: aquasecurity/trivy-action@d23f2e8a2b4b7a3c1d5e6f7a8b9c0d1e2f3a4b5
   ```
3. **Isolate CI runners** — ephemeral, no persistent secrets, network egress filtering
4. **Audit all Actions** — regularly review which Actions your repos use; remove unnecessary ones
5. **Implement SBOMs** — maintain complete software bill of materials to trace dependencies
6. **Monitor CI logs** — alert on unexpected network egress during builds

### Python Packaging Hygiene

1. **Use hash-checking mode** (`pip install --require-hashes`) for production
2. **Pin exact versions** with no `>=` ranges for critical dependencies
3. **Vendor dependencies** or use private PyPI mirrors with curation
4. **Automated scanning** — enable Dependabot, Snyk, or similar for real-time vulnerability alerts
5. **Regular audits** — `pip-audit`, `safety check` in CI

### Cloud Security

1. **IAM least privilege** — CI credentials should have minimal permissions
2. **IMDSv2 enforcement** — require session tokens for EC2 metadata
3. **Workload identity** — use GCP Workload Identity, AWS IAM Roles for Service Accounts instead of keys
4. **Secret scanning** — enable GitHub Advanced Security, GitGuardian, or similar to detect committed secrets
5. **Vault solutions** — HashiCorp Vault, AWS Secrets Manager for dynamic secrets

---

## What We Don't Know (Intelligence Gaps)

- **Full list of affected packages:** Beyond litellm, were other PyPI packages compromised? (Possible given credential access)
- **Attribution:** Who is TeamPCP? Nation-state? Cybercriminal? Hacktivist?
- **Magnitude of data theft:** How many credentials exfiltrated? Any confirmed abuse?
- **Persistence:** Are the backdoors still active in systems that installed malicious litellm? Has the C2 infrastructure been taken down?
- **Next targets:** Will TeamPCP continue to expand to other CI tools (GitLab CI, CircleCI, Jenkins)?

---

## Campaign Assessment

This is not a single vulnerability but a **coordinated, multi-stage campaign**:

1. **CI/CD supply chain poisoning** (Trivy → Checkmarx) provides initial access and credential theft
2. **Downstream package poisoning** (litellm) magnifies impact by orders of magnitude
3. **Kubernetes worm capability** suggests intent for lateral movement and persistence at scale
4. **Credential harvesting** targets cloud infrastructure, potentially enabling ransomware or espionage

**The big picture:** TeamPCP is building a massive botnet of CI/CD pipelines and AI infrastructure. The combination of stolen cloud credentials + backdoored AI packages gives them:
- Compute resources (cryptomining)
- Data access (AI training data, model weights)
- Pivot points into enterprise networks
- Potential for supply chain contamination on an unprecedented scale

**This is arguably the most significant AI ecosystem compromise to date.**

---

## Immediate Actions for Organizations

**If you use ANY AI/cloud tooling (which most do):**

1. **Assume you are affected** until proven otherwise
2. **Rotate ALL credentials** used in CI/CD between Feb 24 - Mar 24
3. **Audit litellm installations** and treat 1.82.7/1.82.8 as compromised hosts
4. **Review CI logs** for signs of credential exfiltration
5. **Check Kubernetes** for suspicious pods or privileged deployments
6. **Enable enhanced monitoring** for cloud API activity unusual times or locations
7. **Subscribe to threat intelligence** for updates on TeamPCP and supply chain threats

---

## Related Intelligence

- **Langflow RCE (CVE-2026-33017)**: Separate but thematically similar — AI workflow platforms under active attack
- **MCP vulnerabilities (CVE-2025-49596, CVE-2026-26118)**: MCP ecosystem also targeted; 40% unpatched
- **n8n RCE (CVE-2026-21858)**: Another AI workflow platform, CVSS 10.0, patched in January

**Pattern:** The entire AI/ML tooling ecosystem is under **coordinated assault** by multiple threat actors. Supply chain attacks are the primary vector.

---

## Timeline Expectation

- **Next 24-48h:** More organizations will report compromises; likely additional packages discovered
- **Next week:** TeamPCP may shift to new targets (GitLab CI, CircleCI, TensorFlow, PyTorch)
- **Next month:** Potential large-scale cryptomining or ransomware campaigns using harvested credentials

---

## References

[1] Sysdig. (2026). "TeamPCP expands: Supply chain compromise spreads from Trivy to Checkmarx GitHub Actions."  
https://www.sysdig.com/blog/teampcp-expands-supply-chain-compromise-spreads-from-trivy-to-checkmarx-github-actions

[2] Snyk. (2026). "How a Poisoned Security Scanner Became the Key to Backdooring LiteLLM."  
https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm/

[3] Arctic Wolf. (2026). "TeamPCP Supply Chain Attack Campaign Targets Trivy, Checkmarx (KICS), and LiteLLM."  
https://arcticwolf.com/resources/blog/teampcp-supply-chain-attack-campaign-targets-trivy-checkmarx-kics-and-litellm/

[4] Microsoft Security. (2026). "Guidance for detecting, investigating, and defending against the Trivy supply chain compromise."  
https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/

[5] ReversingLabs. (2026). "Inside the TeamPCP cascading supply chain attack."  
https://www.reversinglabs.com/blog/teampcp-supply-chain-attack-spreads

[6] GitHub. (2026). "Trivy Action Security Advisory GHSA-9p44-j4g5-cfx5."  
https://github.com/aquasecurity/trivy-action/security/advisories/GHSA-9p44-j4g5-cfx5

[7] Hacker News. (2026). "LiteLLM backdoored via compromised PyPI account."  
https://news.ycombinator.com/item?id=47501729

[8] The Hacker News. (2026). "TeamPCP Hacks Checkmarx GitHub Actions Using Stolen CI Credentials."  
https://thehackernews.com/2026/03/teampcp-hacks-checkmarx-github-actions.html

---

## Next Updates

This report will be updated as new intelligence emerges. Monitor:
- **CISA KEV catalog** for CVE assignments and KEV additions
- **GitHub Security Advisories** for affected repositories
- **Threat intel feeds** from Sysdig, Microsoft, Arctic Wolf, Snyk

**Status:** ACTIVE CAMPAIGN — organizations must respond immediately

---

**Report ID:** TEAMPCP_CAMPAIGN_ANALYSIS_2026-03-28
**Word count:** ~2,300 words
**Classification:** EYES ONLY — Security Operations (read within 12h)
