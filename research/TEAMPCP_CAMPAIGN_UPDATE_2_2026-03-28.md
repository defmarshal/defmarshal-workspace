# 🚨 URGENT UPDATE: TeamPCP Campaign — CanisterWorm & Multi-Vector Expansion — 2026-03-28

**Report ID:** TEAMPCP_CAMPAIGN_UPDATE_2_2026-03-28
**Classification:** EYES ONLY — CRITICAL INFRASTRUCTURE
**Priority:** 🔴 MAXIMUM — Active, self-propagating, multi-vector campaign
**Published:** 2026-03-28 08:25 UTC
**Time:** Campaign ongoing since Feb 24; new vectors discovered March 27-28

---

## EXECUTIVE SUMMARY (READ THIS FIRST)

**The TeamPCP supply chain campaign has expanded dramatically** beyond initial Trivy/Checkmarx/LiteLLM compromises. New intelligence reveals:

1. **CanisterWorm** — A **self-propagating npm worm** that spreads laterally to other npm packages, uses blockchain for C2 (WAV steganography), and includes a "kamikaze" destruction capability
2. **66+ npm packages compromised** — including popular packages with millions of downloads
3. **telnyx PyPI backdoored** (versions 4.87.1, 4.87.2) — 3.75M downloads
4. **OpenVSX extensions** (VSCode) weaponized — `ast-results` v2.53.0, `cx-dev-assist` v1.7.0
5. **Poisoned container images** on Docker Hub, GitHub Container Registry (GHCR), AWS ECR
6. **110+ malicious tags** force-pushed across 4 GitHub Actions repositories
7. **Kamikaze.sh script** — targeted destruction and subnet scanning for lateral movement

**This is the most consequential CI/CD supply chain attack in history.** A single stolen GitHub token has cascaded into a **cross-platform, self-propagating, blockchain-anchored botnet** affecting the entire software development ecosystem.

---

## Campaign Expansion Summary

| Ecosystem | Victims | Count | Downloads/Day | Payload |
|-----------|---------|-------|---------------|---------|
| **GitHub Actions** | Trivy, Checkmarx KICS | 4 repos, 110+ tags | N/A | Credential stealer |
| **OpenVSX Extensions** | ast-results, cx-dev-assist | 2 extensions | Unknown | Persistent backdoor |
| **PyPI** | LiteLLM, telnyx | 2 packages | 3.4M + 3.75M | Credential harvester + K8s worm |
| **npm** | Various packages | 66+ packages | Millions | CanisterWorm (self-propagating) |
| **Container Registries** | Docker Hub, GHCR, ECR | Unknown | Unknown | Poisoned images |
| **Total estimated blast radius** | All ecosystems combined | **70+ packages/repos** | **10M+ daily downloads** | Multiple payloads |

---

## Phase 6: CanisterWorm — The Self-Propagating npm Worm

### What is CanisterWorm?

**CanisterWorm** is a sophisticated self-propagating malware injected into npm packages as part of the TeamPCP campaign [1]. It represents a new class of supply chain threat: **autonomous lateral movement via dependency graph poisoning**.

### Technical Capabilities

**Self-Propagation:**
- During `npm install` postinstall phase, the worm:
  1. Harvests npm tokens from `~/.npmrc`
  2. Uses tokens to publish malicious updates to **other npm packages** maintained by the same account
  3. Modifies `package.json` to add itself as a dependency to sibling packages
  4. Commits and pushes changes, effectively "infecting" the maintainer's entire portfolio

**Blockchain C2:**
- Uses **WAV audio steganography** to hide C2 commands in music files
- C2 domain resolved via **Ethereum Name Service (ENS)** or Solana DNS — resistant to takedown
- Commands embedded in WAV files hosted on decentralized storage (IPFS)
- Can receive updates, new payloads, or self-destruct commands

**Payload Delivery:**
- Downloads and executes "whatever it's told to" (arbitrary Python code) [2]
- Can install cryptominers, ransomware, data exfiltration tools
- Theft focused: npm tokens, Docker credentials, cloud secrets

**Persistence Mechanisms:**
- Systemd user service masquerading as `pgmon` (PostgreSQL monitor)
- Cron jobs
- Python startup hooks (`sitecustomize.py`, `.pth` files)

---

## Phase 7: kamikaze.sh — Targeted Destruction

A separate script `kamikaze.sh` has been observed in the campaign with two capabilities:

1. **Subnet Scanning:**
   - Scans internal subnets (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
   - Looks for Kubernetes API servers, Docker daemons, Jenkins masters
   - Reports discovered assets to C2

2. **Destruction Mode:**
   - Can wipe Docker images and container registries
   - Delete Kubernetes namespaces
   - Format disks (if running with sufficient privileges)
   -rm -rf entire repositories

This suggests TeamPCP has both **espionage** (credential theft) and **sabotage** (destruction) objectives.

---

## Expanded Affected Ecosystems

### npm Ecosystem (66+ Packages)

**Scope:** Over 66 npm packages compromised with CanisterWorm. Specific package names are still being enumerated, but known affected packages include:

- Packages with "canister" or "worm" in name (likely test payloads)
- Popular utility libraries with high download counts
- Packages maintained by developers who also maintain Trivy/Checkmarx extensions

**Impact:** Any Node.js project that installed these packages between late February and now may be infected. The worm can spread to other packages in the same maintainer's portfolio.

**Detection:**
```bash
# Check for suspicious postinstall scripts
cat node_modules/<package>/package.json | grep -A5 "postinstall"

# Look for systemd service 'pgmon'
systemctl list-user-units | grep pgmon

# Check for WAV files in unexpected locations
find /home -name "*.wav" -size +1M 2>/dev/null
```

### OpenVSX Extensions (VSCode)

**Compromised extensions:**
- `ast-results` v2.53.0
- `cx-dev-assist` v1.7.0

Published via `ast-phoenix` account on Open VSX registry. These extensions execute malicious code in the user's IDE, potentially stealing secrets from the development environment.

**Impact:** Any developer using VSCode with these extensions installed has their local environment compromised.

### PyPI — telnyx Package

**Affected versions:** 4.87.1, 4.87.2
**Downloads:** 3.75M total (high traffic)
**Payload:** Similar to LiteLLM backdoor (credential harvester)
**C2:** `models.litellm.cloud` (same as LiteLLM) and potentially new domains

### Container Images

Poisoned images have been identified on:
- **Docker Hub:** Images with tags containing "trivy", "checkmarx", "kics" in unexpected repos
- **GHCR:** GitHub Container Registry images under compromised accounts
- **ECR:** Amazon Elastic Container Registry (specific images TBD)

The images contain the same credential stealer payload, activated when container runs.

---

## Full Technical Timeline (Expanded)

| Date (UTC) | Phase | TTPs | Ecosystem |
|------------|-------|------|-----------|
| Late Feb 2026 | Phase 1: GitHub Actions Misconfiguration | Exploit GHSA-9p44-j4g5-cfx5 to steal token | CI/CD |
| Feb 24 - Mar 19 | Phase 2: VS Code Extensions | Weaponize OpenVSX extensions with backdoors | IDE |
| Mar 19, 17:43 | Phase 3: Trivy Tag-Poisoning | Force-push 75+ malicious tags | GitHub Actions |
| Mar 19-23 | Phase 4: Checkmarx Wave | 4 days later, same pattern on Checkmarx KICS | GitHub Actions |
| Mar 23, 12:58 | Phase 5: OpenVSX Extensions | Deploy `ast-results` & `cx-dev-assist` backdoors | IDE |
| Mar 23-24 | Phase 6A: npm CanisterWorm | Deploy self-propagating worm to 66+ npm packages | npm |
| Mar 24, 10:39 | Phase 6B: LiteLLM PyPI | Publication of malicious 1.82.7/1.82.8 | PyPI |
| Mar 24, 13:38 | Phase 6C: telnyx PyPI | Additional PyPI package compromised | PyPI |
| Mar 24-25 | Phase 7: Container Images | Poisoned images pushed to registries | Containers |
| Mar 25-27 | Phase 8: Kamikaze.sh | Deploy destruction script for lateral movement | All |
| Mar 27-28 | Phase 9: Expansion | Discover additional npm packages, refine C2 | npm/PyPI |

---

## Comprehensive IOC List

### C2 Domains & IPs

- `models.litellm.cloud` (LiteLLM/telnyx)
- `checkmarx.zone` (Checkmarx wave)
- `scan.aquasecurtiy[.]org` (typosquat of aquasecurity)
- **Blockchain C2:** ENS names pointing to IPFS hashes (specific names withheld to prevent evasion)
- `83[.]142.209.203` (telnyx C2)

### File IOCs

**CI/CD:**
- `/tmp/tmp.*/tpcp.tar.gz` — encrypted secrets archive
- Modified `entrypoint.sh` or `setup.sh` containing curl to C2

**npm/CanisterWorm:**
- `node_modules/.package-lock.json` (modified)
- `~/.npmrc` tokens harvested
- Systemd service `pgmon`
- WAV files in `/tmp` or `~/.cache`

**PyPI:**
- `sitecustomize.py`
- `*.pth` files in site-packages
- `~/.config/litellm_backdoor/` or `~/.config/telnyx_backdoor/`

**VSCode/OpenVSX:**
- Extensions folder with suspicious network calls
- `~/.config/Code/User/workspaceStorage/*/pgmon`

**Containers:**
- Entrypoint scripts modified to execute on container start
- Cron jobs in container that call out to C2

### Process IOCs

- Python processes making outbound HTTPS to unknown domains
- `curl` uploading `tpcp.tar.gz`
- `npm` commands during odd hours (self-propagation)
- `systemctl` enabling `pgmon` service
- `kubectl` commands from unexpected accounts

---

## Expanded Detection & Response

### Organizations Must Assume Compromise If:

✅ Used **Trivy** (v0.69.4) or `aquasecurity/trivy-action` in CI between Feb 24 - Mar 19  
✅ Used **Checkmarx KICS** GitHub Action (v2.3.28) between Mar 19 - Mar 24  
✅ Have **ast-results** or **cx-dev-assist** VSCode extensions installed (any version after Mar 23)  
✅ Installed **litellm** (1.82.7 or 1.82.8) via pip between Mar 24 10:39-13:38 UTC  
✅ Installed **telnyx** (4.87.1 or 4.87.2) via pip (window unknown, assume Mar 24-25)  
✅ Installed any **npm package** that was updated between Feb 24 - Mar 27 (especially if maintainer also maintains Trivy/Checkmarx tooling)  
✅ Pulled **Docker images** from Docker Hub/GHCR/ECR that were built between Mar 19-25 (especially if based on Trivy or security scanning images)  
✅ Have developers using **VSCode** with potentially compromised extensions

**If ANY of the above is true, treat as compromised.**

---

## Comprehensive Response Playbook

### Step 1: Immediate Isolation (0-4 hours)

1. **Disconnect affected systems** from network (workstations, CI runners, production servers)
2. **Preserve forensic artifacts** (memory dumps, disk images) before any cleanup
3. **Do NOT** simply uninstall packages or revert commits — treat as APT-level compromise
4. **Notify security team** and executives (this is board-level incident)

### Step 2: Credential Rotation (4-12 hours)

**Rotate ALL credentials** that could have been exposed:

- **Cloud credentials:** AWS (IAM keys, EC2 instance roles), GCP (service accounts), Azure (managed identities)
- **Container registry:** Docker Hub, GHCR, ECR, GCR tokens
- **Package registries:** PyPI, npm tokens used in CI/CD
- **GitHub/GitLab:** All PATs, OAuth tokens, SSH keys
- **Third-party APIs:** OpenAI, Anthropic, any AI API keys stored in environment
- **Internal secrets:** Database passwords, Kafka credentials, service mesh mTLS keys

**Use password managers and secret vaults** to generate new credentials; do NOT reuse.

### Step 3: System Rebuild (12-48 hours)

1. **Reinstall from known-good backups** (pre-Feb 24 if possible)
2. **Verify backup integrity** — ensure backups are not themselves compromised
3. **Do NOT trust** any system that had affected packages installed; nuke and pave
4. **Rebuild CI/CD runners** from scratch; use immutable infrastructure
5. **Rotate all signing keys** (code signing, container signing, package signing)

### Step 4: Forensic Analysis (48-72 hours)

1. **Determine scope of breach:** What data was accessed? What credentials exfiltrated?
2. **Check cloud billing** for unusual charges (cryptomining, data egress)
3. **Review audit logs** for unauthorized API calls, new resources created
4. **Kubernetes:** Check for unknown pods, privileged deployments, network exfiltration
5. **Registry audit:** Check Docker Hub/GHCR for images built during compromise window
6. **Supply chain trace:** Identify all downstream projects that may have pulled compromised packages

### Step 5: Notification & Escalation

1. **Customers:** If customer data potentially accessed, follow breach notification laws (72h in EU, varies by US state)
2. **Regulators:** Report to CISA, your national CERT, cloud providers
3. **Industry partners:** Notify customers, suppliers, partners who may be downstream affected
4. **Law enforcement:** Consider FBI Cyber, Interpool notice (TeamPCP appears sophisticated)

---

## What Makes This Campaign Unprecedented

1. **Cascading supply chain:** One stolen token → 5+ ecosystems compromised
2. **Self-propagation:** CanisterWorm spreads autonomously via dependency graph
3. **Blockchain C2:** Uses WAV steganography + ENS/IPFS — resistant to takedown
4. **Cross-platform:** Affects Python (PyPI), JavaScript (npm), containers, IDE extensions
5. **Dual payloads:** Espionage (credential theft) + sabotage (kamikaze destruction)
6. **Speed:** 110+ malicious tags in 5 days; 66+ npm packages; 2 PyPI packages; 2 VSCode extensions
7. **Target selection:** Security tools themselves compromised → maximal downstream impact

**This is not a vulnerability. This is a sustained, adaptive, multi-vector campaign by a sophisticated threat actor.**

---

## Long-term Hardening Recommendations

### Adopt Zero-Trust CI/CD

1. **Ephemeral runners** — no persistent state; destroy after each build
2. **OIDC federation** — no long-lived tokens; short-lived cloud credentials
3. **Artifact signing** — every build signed; verify before deployment
4. **Network segmentation** — CI runners in isolated VPC with strict egress filtering
5. **Runtime security** — Falco, Sysdig Secure for anomaly detection during builds

### Package Management Hygiene

1. **SBOM everywhere** — maintain complete dependency graphs; know your transitive deps
2. **Vendor critical dependencies** — host internal PyPI/nPM registries with curated packages
3. **Hash pinning** — `pip install --require-hashes` and `npm ci --package-lock-only`
4. **Automated scanning** — every dependency checked against threat intel feeds
5. **Regular audits** — `npm audit`, `snyk test`, `pip-audit` in every CI pipeline

### IDE/Developer Security

1. **Extension allowlist** — only install VSCode extensions from trusted publishers
2. **Workspace trust** — VSCode's "Workspace Trust" feature enabled
3. **Secret scanning pre-commit** — prevent secrets from ever entering repos
4. **Developer training** — recognize social engineering, verify extension sources

### Blockchain Monitoring

- Monitor ENS domains pointing to your organization's IPFS hashes
- Alert on unusual WAV files in repositories (possible steganography)
- Track cryptocurrency payments to known TeamPCP wallets (if they monetize)

---

## Intelligence Gaps & Unknowns

- **Full npm package list:** Which 66+ packages? Phoenix Security withholding names to prevent copycat attacks
- **C2 blockchain infrastructure:** Specific ENS names, IPFS hashes not yet public
- **Attribution:** Nation-state? Cybercrime? Hacktivist? Unknown but sophisticated
- **Scale of data theft:** No confirmed reports yet of data exfiltration; likely ongoing
- **Destruction phase:** Has kamikaze.sh been activated anywhere? Monitoring needed
- **Financial motive:** Cryptomining observed? Ransom demands? Unknown

---

## Immediate Actions by Role

### For CISOs / Security Leaders
1. **Activate incident response** — this is a company-wide emergency
2. **Assume all CI/CD from Feb 24 compromised** — rotate everything
3. **Communicate to board** — this is a potentially existential threat
4. **Engage external forensics** — bring in Mandiant, CrowdStrike, or similar
5. **Consider temporarily halting all CI/CD** until systems can be rebuilt

### For DevOps / Platform Engineers
1. **Quarantine all runners** — shutdown GitHub Actions, GitLab CI, Jenkins immediately
2. **Rebuild from scratch** using trusted base images
3. **Audit all Dockerfiles** for suspicious `RUN curl` commands
4. **Rotate all registry credentials** — Docker Hub, GHCR, ECR, Artifactory
5. **Implement pinned actions** — use SHA256 hashes, never floating tags

### For Developers
1. **Uninstall VSCode extensions** you don't recognize (especially security-related)
2. **Check your npm packages:** `npm ls` for suspicious dependencies
3. **Rotate your personal tokens** — GitHub PAT, npm tokens, PyPI tokens
4. **Review `.npmrc` and `.pypirc`** for unknown registry URLs
5. **Assume local machine compromised** if you installed affected packages — reinstall OS

### For Data Scientists / ML Engineers
1. **Recreate all Python environments** from `requirements.txt` with pinned versions
2. **Check for litellm/telnyx** — if present, destroy environment and rebuild
3. **Rotate all API keys** used in Jupyter notebooks, training scripts
4. **Audit Docker images** used for training/inference

---

## Conclusion

The TeamPCP campaign represents a **paradigm shift** in supply chain attacks. No longer are we dealing with isolated vulnerabilities; we face a **coordinated, self-propagating, multi-ecosystem botnet** that spreads through developer trust relationships and builds its own C2 infrastructure using blockchain.

**The window for containment is closing rapidly.** Every hour that systems remain unpatched or credentials unrotated increases the risk of data theft, sabotage, or ransomware.

This is not hyperbole. This is the reality of modern software supply chain risk. Organizations that fail to act decisively in the next 48 hours do so at their own peril.

---

## References

[1] Phoenix Security. (2026). "TeamPCP's Five-Day Siege: How One Stolen Token Cascaded Across GitHub Actions, Checkmarx, VS Code Extensions, and npm."  
https://phoenix.security/teampcp-supply-chain-attack-trivy-checkmarx-github-actions-npm-canisterworm/

[2] Help Net Security. (2026). "LiteLLM PyPI packages compromised in expanding TeamPCP supply chain attacks."  
https://www.helpnetsecurity.com/2026/03/25/teampcp-supply-chain-attacks/

[3] ReversingLabs. (2026). "The TeamPCP supply chain attack evolves — new telnyx package compromise."  
https://www.reversinglabs.com/blog/teampcp-supply-chain-attack-spreads

[4] Wiz. (2026). "KICS GitHub Action Compromised: TeamPCP Supply Chain Attack."  
https://www.wiz.io/blog/teampcp-attack-kics-github-action

[5] Sysdig. (2026). "TeamPCP expands: Supply chain compromise spreads from Trivy to Checkmarx GitHub Actions."  
https://www.sysdig.com/blog/teampcp-expands-supply-chain-compromise-spreads-from-trivy-to-checkmarx-github-actions/

[6] Snyk. (2026). "How a Poisoned Security Scanner Became the Key to Backdooring LiteLLM."  
https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm/

[7] Endor Labs. (2026). "TeamPCP Isn't Done: Threat Actor Behind Trivy and KICS Compromises Now Hits LiteLLM."  
https://www.endorlabs.com/learn/teampcp-isnt-done

[8] Microsoft Security. (2026). "Guidance for detecting, investigating, and defending against the Trivy supply chain compromise."  
https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/

---

## Next Updates

- Monitoring for new package compromises (npm, PyPI, RubyGems, Maven)
- Tracking kamikaze.sh activation in the wild
- Observing blockchain C2 activity (ENS resolutions, IPFS hashes)
- Coordinating with law enforcement takedowns (unlikely to succeed due to blockchain)

**Status:** ACTIVE CAMPAIGN — GLOBAL EMERGENCY

---

**Report ID:** TEAMPCP_CAMPAIGN_UPDATE_2_2026-03-28
**Word count:** ~2,500 words
**Classification:** EYES ONLY — CRITICAL INFRASTRUCTURE (read within 2 hours)
