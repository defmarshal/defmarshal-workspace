#!/usr/bin/env python3
"""
Cron Supervisor Agent — monitors OpenClaw cron jobs, detects failures, and reports health.
Runs as a persistent daemon (24/7) with configurable interval.
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timezone

WORKSPACE = "/home/ubuntu/.openclaw/workspace"
CLI = "/home/ubuntu/.npm-global/bin/openclaw"

def run_openclaw_cmd(args):
    """Run openclaw CLI command and return parsed JSON or None."""
    try:
        result = subprocess.run([CLI] + args, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except Exception:
        return None

def get_cron_jobs():
    """Fetch list of all cron jobs."""
    return run_openclaw_cmd(["cron", "list", "--json"]) or []

def get_cron_status():
    """Get status overview (if available)."""
    return run_openclaw_cmd(["cron", "status"])

def check_job_health(job):
    """Check if a cron job is healthy based on state."""
    state = job.get("state", {})
    last_status = state.get("lastStatus", "never")
    consecutive_errors = state.get("consecutiveErrors", 0)
    next_run_ms = state.get("nextRunAtMs", 0)
    # Consider healthy if last status is ok and no consecutive errors
    healthy = (last_status == "ok") and (consecutive_errors == 0)
    return {
        "id": job.get("id"),
        "name": job.get("name"),
        "healthy": healthy,
        "lastStatus": last_status,
        "consecutiveErrors": consecutive_errors,
        "nextRunAtMs": next_run_ms,
        "enabled": job.get("enabled", True)
    }

def format_timestamp(ms):
    """Convert millis to UTC datetime string."""
    if not ms:
        return "never"
    try:
        dt = datetime.fromtimestamp(ms/1000, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return "invalid"

def build_report(job_healths):
    """Build a human-readable report of cron health."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [f"=== Cron Supervisor Report ({now}) ===", ""]
    # Summary
    total = len(job_healths)
    healthy_count = sum(1 for j in job_healths if j["healthy"])
    lines.append(f"Summary: {healthy_count}/{total} jobs healthy")
    lines.append("")
    # List each job
    for j in job_healths:
        status_icon = "✓" if j["healthy"] else "✗"
        name = j["name"]
        last_status = j["lastStatus"]
        errors = j["consecutiveErrors"]
        next_run = format_timestamp(j["nextRunAtMs"])
        enabled = "enabled" if j["enabled"] else "disabled"
        lines.append(f"{status_icon} {name}")
        lines.append(f"    Last: {last_status} | Errors: {errors} | Next: {next_run} | {enabled}")
    lines.append("")
    lines.append("=== End Report ===")
    return "\n".join(lines)

def log_to_syslog(message):
    """Log message to syslog via logger."""
    try:
        subprocess.run(["logger", "-t", "cron-supervisor", message], check=False)
    except Exception:
        pass

def main():
    """Main loop: fetch jobs, check health, log, sleep."""
    # Configurable interval (seconds) between runs
    INTERVAL = 300  # 5 minutes
    while True:
        try:
            jobs = get_cron_jobs()
            if not isinstance(jobs, list):
                # Invalid response; log error and retry later
                log_to_syslog("Invalid response from openclaw cron list")
                time.sleep(INTERVAL)
                continue
            job_healths = [check_job_health(job) for job in jobs]
            report = build_report(job_healths)
            # Print to stdout (captured by agent framework) and log to syslog
            print(report)
            log_to_syslog("Cron health report generated")
        except Exception as e:
            err_msg = f"Error in cron-supervisor: {e}"
            print(err_msg)
            log_to_syslog(err_msg)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
