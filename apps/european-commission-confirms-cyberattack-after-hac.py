```python
#!/usr/bin/env python3
"""
EU Commission Cyberattack Simulation: Cloud storage breach detection system.
Demonstrates monitoring, anomaly detection, and incident response workflow.
"""

import os
import time
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set
import random

@dataclass
class FileEvent:
    """Represents a file access or modification event."""
    timestamp: datetime
    file_path: str
    event_type: str  # 'read', 'write', 'delete', 'download'
    user: str
    ip_address: str
    file_size: int
    file_hash: str = ""

@dataclass
class Alert:
    """Represents a security alert."""
    timestamp: datetime
    severity: str  # 'low', 'medium', 'high', 'critical'
    title: str
    description: str
    affected_files: List[str]
    recommended_action: str

class CloudStorageMonitor:
    """Simulates monitoring of cloud storage for suspicious activities."""
    
    def __init__(self, watch_dir: str, baseline_file: str = "baseline.json"):
        self.watch_dir = Path(watch_dir)
        self.baseline_file = self.watch_dir / baseline_file
        self.baseline: Dict[str, str] = {}  # file -> hash
        self.event_log: List[FileEvent] = []
        self.alerts: List[Alert] = []
        self.suspicious_ips: Set[str] = set()
        self.user_activity: Dict[str, List[datetime]] = {}
        
        # Initialize or load baseline
        if self.baseline_file.exists():
            self.load_baseline()
        else:
            self.create_baseline()
    
    def create_baseline(self):
        """Create initial hash baseline of all files."""
        print(f"[*] Creating baseline of {self.watch_dir}...")
        for file_path in self.watch_dir.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.watch_dir))
                self.baseline[rel_path] = self.calculate_hash(file_path)
        self.save_baseline()
        print(f"[+] Baseline created with {len(self.baseline)} files")
    
    def load_baseline(self):
        """Load existing baseline."""
        try:
            with open(self.baseline_file, 'r') as f:
                self.baseline = json.load(f)
        except Exception as e:
            print(f"[!] Failed to load baseline: {e}")
            self.create_baseline()
    
    def save_baseline(self):
        """Save current baseline."""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
    
    def calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "ERROR"
    
    def simulate_file_access(self, file_path: str, event_type: str, user: str, ip: str):
        """Simulate a file access event (would be triggered by real monitoring)."""
        full_path = self.watch_dir / file_path
        if not full_path.exists():
            return
        
        event = FileEvent(
            timestamp=datetime.now(),
            file_path=file_path,
            event_type=event_type,
            user=user,
            ip_address=ip,
            file_size=full_path.stat().st_size,
            file_hash=self.calculate_hash(full_path) if event_type in ['write', 'read'] else ""
        )
        self.event_log.append(event)
        self.check_anomalies(event)
    
    def check_anomalies(self, event: FileEvent):
        """Check if event triggers any security alerts."""
        user = event.user
        now = event.timestamp
        
        # Track user activity
        if user not in self.user_activity:
            self.user_activity[user] = []
        self.user_activity[user].append(now)
        
        # Clean old activity (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.user_activity[user] = [t for t in self.user_activity[user] if t > cutoff]
        
        # Detection rules
        alerts = []
        
        # 1. Bulk download detection: many files accessed in short time
        recent_events = [e for e in self.event_log[-50:] if e.user == user]
        if len(recent_events) > 20 and any(e.event_type == 'read' for e in recent_events[-10:]):
            alerts.append(Alert(
                timestamp=now,
                severity="high",
                title="Bulk Download Detected",
                description=f"User {user} accessed {len(recent_events)} files in recent window",
                affected_files=[e.file_path for e in recent_events[-10:]],
                recommended_action="Review user activity, verify authorization"
            ))
        
        # 2. Unusual IP address
        if ip not in self.trusted_ips():
            self.suspicious_ips.add(ip)
            alerts.append(Alert(
                timestamp=now,
                severity="medium",
                title="Access from Unusual IP",
                description=f"User {user} accessed from unfamiliar IP {ip}",
                affected_files=[event.file_path],
                recommended_action="Verify IP whitelist, consider MFA requirement"
            ))
        
        # 3. Hash mismatch (file tampering)
        if event.event_type == 'write':
            current_hash = event.file_hash
            baseline_hash = self.baseline.get(event.file_path)
            if baseline_hash and current_hash != baseline_hash:
                alerts.append(Alert(
                    timestamp=now,
                    severity="critical",
                    title="File Integrity Violation",
                    description=f"File {event.file_path} modified but hash differs from baseline",
                    affected_files=[event.file_path],
                    recommended_action="IMMEDIATE INVESTIGATION: Potential malware or data exfiltration"
                ))
        
        # 4. After-hours access (outside 9 AM - 6 PM)
        hour = now.hour
        if hour < 9 or hour >= 18:
            alerts.append(Alert(
                timestamp=now,
                severity="low",
                title="After-Hours Access",
                description=f"User {user} accessed files at {now:%H:%M}",
                affected_files=[event.file_path],
                recommended_action="Verify if legitimate off-hours work"
            ))
        
        for alert in alerts:
            self.alerts.append(alert)
            self.print_alert(alert)
    
    def trusted_ips(self) -> List[str]:
        """List of IPs that should have access (simulated)."""
        return ["10.0.1.100", "10.0.1.101", "10.0.1.102", "192.168.1.50"]
    
    def print_alert(self, alert: Alert):
        """Display alert to console."""
        severity_color = {
            'low': '\033[93m',    # yellow
            'medium': '\033[93m', # yellow
            'high': '\033[91m',   # red
            'critical': '\033[91m\033[1m'  # bold red
        }
        reset = '\033[0m'
        color = severity_color.get(alert.severity, '')
        
        print(f"\n{color}[{alert.severity.upper()}] {alert.title}{reset}")
        print(f"    Time: {alert.timestamp}")
        print(f"    Desc: {alert.description}")
        print(f"    Files: {', '.join(alert.affected_files)}")
        print(f"    Action: {alert.recommended_action}")
    
    def generate_incident_report(self) -> str:
        """Generate a summary report of recent alerts."""
        if not self.alerts:
            return "No security incidents detected."
        
        report = []
        report.append("="*60)
        report.append("SECURITY INCIDENT REPORT")
        report.append(f"Generated: {datetime.now()}")
        report.append(f"Total alerts: {len(self.alerts)}")
        report.append("-"*60)
        
        by_severity = {}
        for alert in self.alerts:
            by_severity.setdefault(alert.severity, []).append(alert)
        
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in by_severity:
                report.append(f"\n{severity.upper()} ({len(by_severity[severity])})")
                for alert in by_severity[severity][-3:]:  # Show last 3 of each
                    report.append(f"  - {alert.timestamp}: {alert.title}")
                    if alert.affected_files:
                        report.append(f"    Files: {len(alert.affected_files)} affected")
        
        report.append("\n" + "="*60)
        return "\n".join(report)

def simulate_attack_scenario():
    """
    Simulate a cyberattack on EU Commission cloud storage:
    - Baseline established
    - Normal user activity
    - Attacker gains access via compromised credentials
    - Bulk download of sensitive documents
    - File tampering
    - Alerts triggered
    """
    print("="*60)
    print("EU COMMISSION CLOUD STORAGE BREACH SIMULATION")
    print("="*60)
    print()
    
    # Setup monitoring environment
    monitor = CloudStorageMonitor("/tmp/eu_commission_cloud")
    
    # Create some sample files
    sample_files = [
        "policy/eu_ai_act_draft_2026.pdf",
        "policy/member_state_compliance_reports.xlsx",
        "personal/commissioner_contacts.json",
        "budget/2026_appropriations.xlsx",
        "diplomatic/negotiation_notes_us_trade.md"
    ]
    
    watch_dir = monitor.watch_dir
    watch_dir.mkdir(exist_ok=True)
    
    print("[PHASE 1] Normal Operations")
    print("-"*40)
    # Simulate normal user activity
    normal_user = "john.doe@ec.europa.eu"
    normal_ip = "10.0.1.100"
    
    for i, fpath in enumerate(sample_files):
        full = watch_dir / fpath
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(f"EU Commission document #{i+1}\nConfidential\n")
        monitor.baseline[str(fpath)] = monitor.calculate_hash(full)
        monitor.simulate_file_access(fpath, 'write', normal_user, normal_ip)
        time.sleep(0.1)
    
    monitor.save_baseline()
    print(f"[+] Normal operation: {len(sample_files)} files created by {normal_user}")
    time.sleep(1)
    
    print("\n[PHASE 2] Attacker Compromises Account")
    print("-"*40)
    attacker_user = normal_user  # Attacker using stolen credentials
    attacker_ip = "185.220.101.45"  # Suspicious external IP
    
    print(f"[!] Attacker logs in as {attacker_user} from {attacker_ip}")
    print("[!] Session started at", datetime.now().strftime("%H:%M:%S"))
    
    # Attacker enumerates and downloads sensitive files
    time.sleep(1)
    print("[!] Enumerating sensitive files...")
    
    sensitive_targets = sample_files[:3]  # Target top 3 most sensitive
    
    for fpath in sensitive_targets:
        monitor.simulate_file_access(fpath, 'read', attacker_user, attacker_ip)
        time.sleep(0.2)
    
    time.sleep(1)
    
    print("[!] Initiating bulk download...")
    # Bulk download - trigger high-severity alert
    for _ in range(25):
        fpath = random.choice(sample_files)
        monitor.simulate_file_access(fpath, 'read', attacker_user, attacker_ip)
        time.sleep(0.05)
    
    time.sleep(1)
    
    print("[!] Tampering with file to cover tracks...")
    # Modify a file - trigger critical alert
    tamper_file = sample_files[0]
    full = watch_dir / tamper_file
    full.write_text("MODIFIED BY ATTACKER\nOriginal content erased\n")
    monitor.simulate_file_access(tamper_file, 'write', attacker_user, attacker_ip)
    monitor.baseline[tamper_file] = monitor.calculate_hash(full)  # Update baseline to avoid repeat alerts
    
    time.sleep(1)
    
    print("[!] Exfiltration complete. Logging out.")
    
    print("\n[PHASE 3] Security Response")
    print("-"*40)
    time.sleep(2)
    
    # Generate incident report
    report = monitor.generate_incident_report()
    print(report)
    
    print("\n[RESPONSE ACTIONS]")
    print("1. Incident response team notified")
    print("2. Compromised account disabled")
    print("3. IP address blocked at firewall")
    print("4. Forensic preservation of logs")
    print("5. Password reset for affected user")
    print("6. Review of files accessed for data classification")
    print("7. Potential data breach notification to EU DPO")
    print("8. Investigation of lateral movement")
    
    print("\n" + "="*60)
    print("SIMULATION COMPLETE")
    print("In a real scenario, the Commission would now:")
    print("- Notify ENISA and relevant DPAs")
    print("- Assess personal data breach under GDPR")
    print("- Coordinate with Europol and member states")
    print("- Issue public communication if required")
    print("="*60)
    
    # Cleanup
    import shutil
    shutil.rmtree(watch_dir)

if __name__ == "__main__":
    random.seed(42)
    simulate_attack_scenario()
```