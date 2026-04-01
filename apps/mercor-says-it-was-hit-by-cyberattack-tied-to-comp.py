```python
#!/usr/bin/env python3
"""
Mercor Security Incident Response Simulator
Detects compromised open-source dependencies (e.g., LiteLLM) in Python environments.
"""

import subprocess
import sys
import json
from datetime import datetime

# Simulated threat intelligence: known compromised packages and versions
COMPROMISED_PACKAGES = {
    "litellm": {
        "compromised_versions": ["0.1.0", "0.1.1", "0.1.2"],
        "cve": "CVE-2026-XXXX",
        "attack_vector": "Malicious code injection via PyPI",
        "impact": "Data exfiltration, credential theft",
        "discovery_date": "2026-03-30",
    },
    "requests": {
        "compromised_versions": ["2.28.0", "2.28.1"],
        "cve": "CVE-2025-XXXX",
        "attack_vector": "Typosquatting supply chain attack",
        "impact": "Potential remote code execution",
        "discovery_date": "2025-11-15",
    },
}

def get_installed_packages():
    """Return dict of package -> version using pip list --format=json."""
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        packages = json.loads(output)
        return {pkg["name"].lower(): pkg["version"] for pkg in packages}
    except Exception:
        return {}

def check_for_compromised(packages):
    """Check installed packages against compromised threat intel."""
    findings = []
    for pkg, version in packages.items():
        if pkg in COMPROMISED_PACKAGES:
            info = COMPROMISED_PACKAGES[pkg]
            if version in info["compromised_versions"]:
                findings.append({
                    "package": pkg,
                    "installed_version": version,
                    "compromised_versions": info["compromised_versions"],
                    "cve": info["cve"],
                    "attack_vector": info["attack_vector"],
                    "impact": info["impact"],
                    "discovery_date": info["discovery_date"],
                })
    return findings

def generate_report(findings):
    """Print a concise security incident response report."""
    print("=" * 60)
    print("MERCOR SECURITY INCIDENT RESPONSE")
    print("=" * 60)
    print(f"Scan timestamp: {datetime.utcnow().isoformat()} UTC")
    print("Scenario: Compromise via open-source LiteLLM dependency")
    print("-" * 60)
    
    if not findings:
        print("✅ No known compromised packages detected in current environment.")
        print("System appears clean based on available threat intelligence.")
        return
    
    print("🚨 CRITICAL: Compromised dependencies found!")
    print()
    for i, f in enumerate(findings, 1):
        print(f"[{i}] {f['package'].upper()} (v{f['installed_version']})")
        print(f"    CVE: {f['cve']} | Discovered: {f['discovery_date']}")
        print(f"    Attack vector: {f['attack_vector']}")
        print(f"    Impact: {f['impact']}")
        print(f"    Affected versions: {', '.join(f['compromised_versions'])}")
        print()
    
    print("IMMEDIATE ACTIONS:")
    print("1. Isolate affected systems from network (air gap if possible)")
    print("2. Preserve logs; check for data exfiltration signs")
    print("3. Roll back to a safe version: pip install --force-reinstall <package>==<safe_version>")
    print("4. Rotate all secrets, API keys, and credentials")
    print("5. Notify stakeholders and legal team (extortion crew may have data)")
    print("6. Review dependency management: use verified indices, pin versions, scan with SCA tools")
    print("=" * 60)

def main():
    packages = get_installed_packages()
    if not packages:
        print("Unable to retrieve installed packages. Is pip available?")
        return
    findings = check_for_compromised(packages)
    generate_report(findings)

if __name__ == "__main__":
    main()
```