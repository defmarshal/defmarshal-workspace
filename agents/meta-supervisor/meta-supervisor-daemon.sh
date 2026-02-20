#!/usr/bin/env bash
# Meta-Supervisor Daemon
# Continuous agent outcome auditor running 24/7

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

WORKSPACE=$(pwd)
REPORT_DIR="$WORKSPACE/agents/meta-supervisor/reports"
LOG_DIR="$WORKSPACE/agents/meta-supervisor/logs"
mkdir -p "$REPORT_DIR" "$LOG_DIR"

timestamp=$(date +%Y-%m-%d_%H%M)
log_file="$LOG_DIR/meta-supervisor-daemon-${timestamp}.log"
pid_file="$WORKSPACE/agents/meta-supervisor/.meta-supervisor.pid"

log() {
  echo "[$(date --iso-8601=seconds)] $*" | tee -a "$log_file"
}

# Write PID
if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
  log "Meta-Supervisor daemon already running (PID $(cat "$pid_file"))"
  exit 0
fi
echo $$ > "$pid_file"
log "Meta-Supervisor daemon starting (PID $$)"

# Configuration
INTERVAL_MINUTES=${INTERVAL_MINUTES:-60}
STALENESS_HOURS=${STALENESS_HOURS:-4}
MIN_OUTPUT_CHANGES=${MIN_OUTPUT_CHANGES:-1}

log "Interval: ${INTERVAL_MINUTES} minutes"
log "Staleness threshold: ${STALENESS_HOURS} hours"

# Trap exit to clean up PID
cleanup() {
  log "Meta-Supervisor daemon stopping"
  rm -f "$pid_file"
  exit 0
}
trap cleanup INT TERM EXIT

# Main loop
while true; do
  cycle_start=$(date +%s)
  log "=== Cycle starting ==="

  # Run one audit cycle (reuse the Python logic)
  if ! python3 - <<'PY' 2>&1 | tee -a "$log_file"
import json, sys, os, time, datetime, glob
workspace = sys.argv[1]
staleness_hours = float(sys.argv[2])
now = time.time()
staleness_sec = staleness_hours * 3600

# fetch cron jobs via openclaw
import subprocess
result = subprocess.run(['openclaw','cron','list','--json'], capture_output=True, text=True)
if result.returncode != 0:
    print(f"ERROR: openclaw cron list failed: {result.stderr}")
    sys.exit(1)
data = json.loads(result.stdout)
jobs = data.get('jobs', [])

# purposes map
PURPOSES = {
    "agni-cron": "Brainstorm improvements and spawn Rudra",
    "dev-agent-cron": "Continuous development of tools and infrastructure",
    "content-agent-cron": "Create anime summaries, tech writeups, daily digests",
    "research-agent-cron": "Conduct research on anime, banking, tech, AI",
    "workspace-builder": "Strategic workspace improvements and planning",
    "supervisor-cron": "Monitor system health and alert on issues",
    "agent-manager-cron": "Manage agent lifecycles and maintenance",
    "vishwakarma-cron": "Plan game development projects",
    "meta-agent-cron": "Meta-tasks: memory reindex, housekeeping",
    "meta-supervisor-cron": "Audit agent outcomes and alignment",
    "notifier-cron": "Send notifications and reminders",
    "random-torrent-downloader": "Random torrent additions",
    "daily-digest-cron": "Generate daily summary digest",
    "content-index-update-cron": "Refresh content archive index",
    "git-janitor-cron": "Auto-commit and push changes",
    "memory-reindex-cron": "Reindex memory stores",
    "log-rotate-cron": "Rotate logs",
    "cleanup-downloads-cron": "Prune old downloads",
    "backup-cleanup-cron": "Clean old backups",
    "auto-torrent-cron": "Add anime torrents",
    "cleanup-agent-artifacts-cron": "Clean stale agent artifacts",
    "archiver-manager-cron": "Manage archives",
}

def check_agent(job):
    name = job.get('name', 'unknown')
    payload = job.get('payload', {})
    last_run = job.get('state', {}).get('lastRunAtMs', 0)
    last_status = job.get('state', {}).get('lastStatus', 'unknown')
    consecutive_errors = job.get('state', {}).get('consecutiveErrors', 0)

    last_run_sec = last_run / 1000.0 if last_run else 0
    age_sec = now - last_run_sec if last_run_sec else float('inf')
    stale = age_sec > staleness_sec

    findings = []
    outcome = "ok"
    if last_status != 'ok':
        outcome = "failed"
        findings.append(f"Last status: {last_status}")
    if consecutive_errors > 0:
        findings.append(f"Consecutive errors: {consecutive_errors}")
    if stale:
        outcome = "stale"
        findings.append(f"Last run {age_sec/3600:.1f}h ago (> {staleness_hours}h)")

    # Agent-specific checks
    expected_report = None
    expected_log = None

    if name == "agni-cron":
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_plans = [p for p in glob.glob(f"{workspace}/agents/agni/plans/plan-{today_str}_*.md")]
        if not today_plans:
            findings.append("No plans today")
            outcome = "no_output"
        else:
            newest_plan = max(today_plans, key=os.path.getmtime)
            newest_plan_ts = os.path.getmtime(newest_plan)
            base = os.path.basename(newest_plan).replace('plan-','').replace('.md','')
            expected_report = f"{workspace}/agents/rudra/reports/report-{base}.md"
            expected_log = f"{workspace}/agents/rudra/logs/exec-{base}.log"
            report_exists = os.path.exists(expected_report)
            log_exists = os.path.exists(expected_log)
            if not (report_exists and log_exists):
                age_h = (now - newest_plan_ts) / 3600
                if age_h < 2:
                    findings.append(f"Recent plan (within 2h) pending Rudra; not flagged")
                else:
                    outcome = "no_output"
                    if not report_exists:
                        findings.append(f"Missing report: {os.path.basename(expected_report)}")
                    if not log_exists:
                        findings.append(f"Missing log: {os.path.basename(expected_log)}")
    elif name == "content-agent-cron":
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_content = [c for c in glob.glob(f"{workspace}/content/{today_str}*.md")]
        if not today_content:
            findings.append("No content files today")
            outcome = "no_output"
        else:
            newest_mtime = max(os.path.getmtime(c) for c in today_content)
            if newest_mtime < now - 12*3600:
                findings.append("Latest content >12h old (agent may be idle)")
    elif name == "research-agent-cron":
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_research = [r for r in glob.glob(f"{workspace}/research/{today_str}*.md")]
        if not today_research:
            findings.append("No research files today")
            outcome = "no_output"
        else:
            newest_mtime = max(os.path.getmtime(r) for r in today_research)
            if newest_mtime < now - 12*3600:
                findings.append("Latest research >12h old")
    elif name == "daily-digest-cron":
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        digest_file = f"{workspace}/reports/{today_str}-daily-digest.md"
        if not os.path.exists(digest_file):
            findings.append("Daily digest report not found in reports/")
            outcome = "no_output"
        else:
            digest_mtime = os.path.getmtime(digest_file)
            if digest_mtime < last_run_sec:
                findings.append("Daily digest report not updated after last run")
                outcome = "no_output"

    # Generic checks
    if expected_report and not os.path.exists(expected_report):
        findings.append(f"Missing report: {os.path.basename(expected_report)}")
    if expected_log and not os.path.exists(expected_log):
        findings.append(f"Missing log: {os.path.basename(expected_log)}")

    return {
        "name": name,
        "purpose": PURPOSES.get(name, "Unknown"),
        "last_run_ms": last_run,
        "age_h": age_sec/3600,
        "status": last_status,
        "errors": consecutive_errors,
        "outcome": outcome,
        "findings": findings
    }

results = [check_agent(job) for job in jobs]

# Generate report
report_date = datetime.date.today().isoformat()
report_file = f"{workspace}/agents/meta-supervisor/reports/report-{report_date}.md"
report_lines = [
    f"# Meta-Supervisor Report — {report_date}",
    "",
    "## Agent Status",
    "",
    "| Agent | Purpose | Last Run | Status | Errors | Outcome | Findings |",
    "|-------|---------|----------|--------|--------|---------|----------|"
]
for r in results:
    last_run_str = datetime.datetime.fromtimestamp(r['last_run_ms']/1000).strftime('%H:%M') if r['last_run_ms'] else "never"
    findings_str = "; ".join(r['findings']) if r['findings'] else "-"
    report_lines.append(f"| {r['name']} | {r['purpose']} | {last_run_str} | {r['status']} | {r['errors']} | **{r['outcome']}** | {findings_str} |")

alerts = [r for r in results if r['outcome'] in ('failed', 'stale', 'no_output')]
report_lines.extend(["", "## Alerts", ""])
if alerts:
    for a in alerts:
        report_lines.append(f"- **{a['name']}**: {a['outcome']} — {'; '.join(a['findings'])}")
else:
    report_lines.append("All agents nominal.")

report_lines.extend(["", "## Summary", f"- Total agents monitored: {len(results)}", f"- Issues detected: {len(alerts)}", ""])
with open(report_file, 'w') as f:
    f.write("\n".join(report_lines))

print(f"Report generated: {os.path.basename(report_file)}")
print("Meta-Supervisor cycle completed")
sys.exit(0)
PY "$workspace" "$staleness_hours"
  then
    log "Cycle completed successfully"
  else
    log "Cycle failed with exit code $?; will retry next interval"
  fi

  # Compute sleep time to maintain fixed interval
  cycle_end=$(date +%s)
  elapsed=$((cycle_end - cycle_start))
  sleep_seconds=$(( INTERVAL_MINUTES * 60 - elapsed ))
  if [ "$sleep_seconds" -gt 0 ]; then
    log "Sleeping ${sleep_seconds}s until next cycle"
    sleep "$sleep_seconds"
  else
    log "Cycle overran interval by $(( -sleep_seconds ))s; next cycle starting immediately"
  fi
done
