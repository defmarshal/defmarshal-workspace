```python
#!/usr/bin/env python3
"""
Anthropic Incident Tracker
Track human borks at Anthropic - because safety is important!
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

class AnthropicBorkTracker:
    def __init__(self, storage_path="anthropic_borks.json"):
        self.storage = Path(storage_path)
        self.incidents = self.load()
        self.bork_types = [
            "Pushed to prod without testing",
            "Deleted main database backup",
            "Committed AWS secret to GitHub",
            "Misconfigured firewall exposing internal services",
            "Introduced memory leak in core service",
            "Disabled monitoring and forgot to re-enable",
            "Ran 'rm -rf' on wrong server",
            "Changed clock sync causing cascade failures",
            "Deployed untested AI weights causing toxic outputs",
            "Broke CI/CD with untested PR",
            "Lost encryption keys for customer data",
            "Overloaded DB with unindexed query",
            "Misrouted traffic to test environment",
            "Forced restart of all nodes causing downtime",
            "Scaled critical service to zero",
            "Introduced race condition causing corruption",
            "Misconfigured autoscaling infinite loop",
            "Deployed code with infinite loop",
            "Forgot to renew SSL certificates",
            "Broke OAuth integration"
        ]
    
    def load(self):
        if self.storage.exists():
            try:
                return json.loads(self.storage.read_text())
            except:
                return []
        return []
    
    def save(self):
        self.storage.write_text(json.dumps(self.incidents, indent=2))
    
    def add_bork(self, description=None, severity="medium"):
        bork = {
            "id": len(self.incidents) + 1,
            "timestamp": datetime.now().isoformat(),
            "description": description or random.choice(self.bork_types),
            "severity": severity,
            "human": "Definitely a human error"
        }
        self.incidents.append(bork)
        self.save()
        return bork
    
    def get_stats(self, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        recent = [i for i in self.incidents if datetime.fromisoformat(i["timestamp"]) > cutoff]
        by_severity = {}
        for inc in recent:
            by_severity[inc["severity"]] = by_severity.get(inc["severity"], 0) + 1
        return {
            "total_borks": len(recent),
            "by_severity": by_severity,
            "borks_per_day": len(recent) / days if days > 0 else 0
        }
    
    def generate_report(self):
        stats = self.get_stats(30)  # last 30 days
        print("\n" + "="*60)
        print("ANTHROPIC INCIDENT REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        print(f"Total borks (last 30 days): {stats['total_borks']}")
        print(f"Borks per day average: {stats['borks_per_day']:.2f}")
        if stats['by_severity']:
            print("\nBy severity:")
            for sev, count in sorted(stats['by_severity'].items()):
                print(f"  {sev}: {count}")
        
        # Check if it's "having a month"
        if stats['total_borks'] > 20:
            print("\n🚨 ALERT: Anthropic is having a month! 🚨")
            print("Multiple critical incidents in short period.")
            print("Consider immediate safety review and process overhaul.")
        elif stats['total_borks'] > 10:
            print("\n⚠️  WARNING: Elevated incident rate")
            print("Monitor closely and investigate root causes.")
        else:
            print("\n✅ Incident rate within normal parameters")
        
        # Show recent incidents
        recent = sorted(self.incidents, key=lambda x: x["timestamp"], reverse=True)[:5]
        if recent:
            print("\nMost recent borks:")
            for inc in recent:
                date = datetime.fromisoformat(inc["timestamp"]).strftime("%m-%d %H:%M")
                print(f"  [{date}] [{inc['severity'].upper()}] {inc['description']}")

def demo_day_in_the_life():
    """Simulate a chaotic day at Anthropic where multiple borks happen."""
    tracker = AnthropicBorkTracker()
    
    print("Simulating a 'human really borks things' day at Anthropic...")
    incidents = [
        ("Pushed to prod without running tests", "high"),
        ("Committed AWS secret key to public GitHub repo", "critical"),
        ("Disabled monitoring during maintenance and forgot to re-enable", "medium"),
        ("Deployed untested model weights causing toxic outputs", "critical"),
        ("Ran 'rm -rf' on wrong server (but had backups)", "high"),
    ]
    
    for desc, sev in incidents:
        tracker.add_bork(description=desc, severity=sev)
        print(f"  Bork logged: {desc}")
    
    tracker.generate_report()

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        tracker = AnthropicBorkTracker()
        
        if command == "add":
            desc = sys.argv[2] if len(sys.argv) > 2 else None
            sev = sys.argv[3] if len(sys.argv) > 3 else "medium"
            bork = tracker.add_bork(desc, sev)
            print(f"Logged bork #{bork['id']}: {bork['description']}")
        
        elif command == "report":
            tracker.generate_report()
        
        elif command == "demo":
            demo_day_in_the_life()
        
        else:
            print("Usage: anthropic-tracker [add <desc> <severity>|report|demo]")
    else:
        print("Anthropic Incident Tracker")
        print("Commands: add, report, demo")
        print("Example: anthropic-tracker add 'Forgot to rotate keys' high")
        demo_day_in_the_life()

if __name__ == "__main__":
    main()
```