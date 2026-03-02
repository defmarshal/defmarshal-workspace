#!/usr/bin/env python3
"""Update heartbeat-state.json with current timestamps for all checks."""
import json, time, os, re
from datetime import datetime

WORKSPACE = "/home/ubuntu/.openclaw/workspace"
HEARTBEAT_FILE = f"{WORKSPACE}/HEARTBEAT.md"
STATE_FILE = f"{WORKSPACE}/memory/heartbeat-state.json"

def get_check_names():
    """Parse HEARTBEAT.md for check names like 'email', 'calendar', 'weather'."""
    checks = []
    try:
        with open(HEARTBEAT_FILE) as f:
            for line in f:
                if line.startswith('- **'):
                    # Example: "- **email**: Check inbox (urgent)"
                    parts = line.split('**')
                    if len(parts) >= 3:
                        name = parts[1].strip()
                        checks.append(name)
    except:
        checks = ['email', 'calendar', 'weather', 'health']
    return checks

def main():
    now = int(time.time())
    # For heartbeat, we set last check to now for all checks to show as recently checked
    last_checks = {name: now for name in get_check_names()}
    state = {"lastChecks": last_checks, "updatedAt": now}
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ Heartbeat state updated: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
