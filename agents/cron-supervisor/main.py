#!/usr/bin/env python3
"""
Cron Supervisor Agent — reads ~/.openclaw/cron/jobs.json directly to avoid CLI deadlock.
Generates a concise health report every run.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

JOBS_JSON = Path.home() / ".openclaw" / "cron" / "jobs.json"
WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
LOG_PATH = WORKSPACE / "memory" / "cron-supervisor.log"

def read_jobs():
    try:
        with open(JOBS_JSON, "r") as f:
            data = json.load(f)
        return data.get("jobs", [])
    except Exception as e:
        print(f"ERROR: Cannot read cron jobs: {e}", file=sys.stderr)
        return []

def check_health(job):
    state = job.get("state", {})
    last_status = state.get("lastStatus", "never")
    consecutive_errors = state.get("consecutiveErrors", 0)
    next_run_ms = state.get("nextRunAtMs", 0)
    healthy = (last_status == "ok") and (consecutive_errors == 0)
    return {
        "name": job.get("name"),
        "healthy": healthy,
        "lastStatus": last_status,
        "consecutiveErrors": consecutive_errors,
        "nextRunAtMs": next_run_ms,
        "enabled": job.get("enabled", True)
    }

def fmt_ms(ms):
    if not ms:
        return "never"
    try:
        dt = datetime.fromtimestamp(ms/1000, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return "invalid"

def build_report(healths):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    total = len(healths)
    healthy = sum(1 for h in healths if h["healthy"])
    lines = [f"=== Cron Health Report ({now}) ===", f"Summary: {healthy}/{total} jobs healthy", ""]
    # Failures first
    failures = [h for h in healths if not h["healthy"]]
    if failures:
        lines.append("!!! FAILURES !!!")
        for f in failures:
            lines.append(f"✗ {f['name']}: status={f['lastStatus']}, errors={f['consecutiveErrors']}, next={fmt_ms(f['nextRunAtMs'])}")
        lines.append("")
    # Compact list
    for h in healths:
        icon = "✓" if h["healthy"] else "✗"
        lines.append(f"{icon} {h['name']} (errors={h['consecutiveErrors']}, next={fmt_ms(h['nextRunAtMs'])})")
    lines.append("=== End Report ===")
    return "\n".join(lines)

def log_report(report):
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(report + "\n")
    except Exception:
        pass

def main():
    jobs = read_jobs()
    if not jobs:
        print("WARNING: No cron jobs found or cannot read jobs.json")
    healths = [check_health(job) for job in jobs]
    report = build_report(healths)
    print(report)
    log_report(report)

if __name__ == "__main__":
    main()
