#!/usr/bin/env bash
# Meta-Supervisor Cycle
# Audits other agents' health and outcome alignment

set -euo pipefail
cd /home/ubuntu/.openclaw/workspace

WORKSPACE=$(pwd)
REPORT_DIR="$WORKSPACE/agents/meta-supervisor/reports"
LOG_DIR="$WORKSPACE/agents/meta-supervisor/logs"
mkdir -p "$REPORT_DIR" "$LOG_DIR"

timestamp=$(date +%Y-%m-%d_%H%M)
log_file="$LOG_DIR/meta-supervisor-${timestamp}.log"
report_file="$REPORT_DIR/report-$(date +%Y-%m-%d).md"

log() {
  echo "[$(date --iso-8601=seconds)] $*" | tee -a "$log_file"
}

log "Meta-Supervisor cycle starting"

# Load thresholds (can be overridden via env)
STALENESS_HOURS=${STALENESS_HOURS:-4}
MIN_OUTPUT_CHANGES=${MIN_OUTPUT_CHANGES:-1}

# Fetch cron jobs via openclaw
if ! command -v openclaw &>/dev/null; then
  log "ERROR: openclaw CLI not found"
  exit 1
fi

cron_json=$(openclaw cron list --json 2>&1) || {
  log "ERROR: Failed to get cron list"
  echo "$cron_json" >> "$log_file"
  exit 1
}
# Strip any non-JSON preamble (Doctor warnings)
cron_json=$(echo "$cron_json" | sed -n '/^{/,$p')

# Parse cron JSON with python3 (safe)
python3 - <<'PY' "$cron_json" "$WORKSPACE" "$STALENESS_HOURS" "$MIN_OUTPUT_CHANGES" "$REPORT_DIR" "$LOG_DIR" "$timestamp" 2>&1 | tee -a "$log_file"
import json, sys, os, subprocess, time, datetime, glob
cron_json = sys.argv[1]
workspace = sys.argv[2]
staleness_hours = int(sys.argv[3])
min_changes = int(sys.argv[4])
report_dir = sys.argv[5]
log_dir = sys.argv[6]
timestamp = sys.argv[7]

now = time.time()
staleness_sec = staleness_hours * 3600

try:
    data = json.loads(cron_json)
    jobs = data.get('jobs', [])
except Exception as e:
    print(f"ERROR: Failed to parse cron JSON: {e}")
    sys.exit(1)

# Map of known agent purposes (can be expanded)
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

# Helper to read latest files matching pattern
def latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    # Sort by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]

# Agent check logic
def check_agent(job):
    name = job.get('name', 'unknown')
    payload = job.get('payload', {})
    last_run = job.get('state', {}).get('lastRunAtMs', 0)
    last_status = job.get('state', {}).get('lastStatus', 'unknown')
    consecutive_errors = job.get('state', {}).get('consecutiveErrors', 0)

    # Convert ms to seconds
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
    report_exists = False
    log_exists = False
    changes_count = 0
    expected_report = None
    expected_log = None

    if name == "agni-cron":
        # Check that the most recent plan has a corresponding Rudra report/log,
        # but allow a grace period of 2 hours after the plan before flagging.
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_plans = [p for p in glob.glob(f"{workspace}/agents/agni/plans/plan-{today_str}_*.md")]
        if not today_plans:
            findings.append("No plans today")
            outcome = "no_output"
        else:
            # Get the newest plan by modification time
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
    elif name in ("dev-agent-cron", "workspace-builder"):
        # Check for recent commits by this agent (within 1 day)
        # Use git log with since and author/prefix is complex; we'll just check if there are any recent commits at all
        # For simplicity, check git status? Not reliable. We'll skip deep commit check.
        pass
    if name == "content-agent-cron":
        # Check for any content file dated today that is not older than 12 hours
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_content = [c for c in glob.glob(f"{workspace}/content/{today_str}*.md")]
        if not today_content:
            findings.append("No content files today")
            outcome = "no_output"
        else:
            # Check if the newest content is within 12 hours (agent may have already produced work)
            newest_mtime = max(os.path.getmtime(c) for c in today_content)
            if newest_mtime < now - 12*3600:
                findings.append("Latest content >12h old (agent may be idle)")
                # not necessarily no_output; keep outcome as ok if fresh enough content exists
            # else ok
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
            # else ok
    elif name == "daily-digest-cron":
        # Daily digest is generated by daily-digest-cron into reports/ (not content/)
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        digest_file = f"{workspace}/reports/{today_str}-daily-digest.md"
        if not os.path.exists(digest_file):
            findings.append("Daily digest report not found in reports/")
            outcome = "no_output"
        else:
            digest_mtime = os.path.getmtime(digest_file)
            # Debug: print values to stderr (goes to log)
            print(f"[DEBUG daily-digest] workspace={workspace}, digest_file={digest_file}, exists=True, digest_mtime={digest_mtime}, last_run_sec={last_run_sec}, digest_newer={digest_mtime > last_run_sec}", file=sys.stderr)
            # Expect it to be updated after last run; if not, investigate
            if digest_mtime < last_run_sec:
                findings.append("Daily digest report not updated after last run")
                outcome = "no_output"
    # Add more agent checks as needed...

    # Generic log/report presence from known patterns
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

# Process all cron jobs
results = []
for job in jobs:
    info = check_agent(job)
    results.append(info)

# Generate report
report_date = datetime.date.today().isoformat()
report_file = os.path.join(report_dir, f"report-{report_date}.md")
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

report_lines.extend(["", "## Alerts", ""])
alerts = [r for r in results if r['outcome'] in ('failed', 'stale', 'no_output')]
if alerts:
    for a in alerts:
        report_lines.append(f"- **{a['name']}**: {a['outcome']} — {'; '.join(a['findings'])}")
else:
    report_lines.append("All agents nominal.")

report_lines.extend(["", "## Summary", f"- Total agents monitored: {len(results)}", f"- Issues detected: {len(alerts)}", ""])
report_content = "\n".join(report_lines)

# Write report
with open(report_file, 'w') as f:
    f.write(report_content)

print(f"Report generated: {os.path.basename(report_file)}")
print("Meta-Supervisor cycle completed")
sys.exit(0)
PY
