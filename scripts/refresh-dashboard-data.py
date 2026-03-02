#!/usr/bin/env python3
"""Refresh dashboard data.json with latest info."""
import json, time, subprocess, os, glob, re, sys
from datetime import datetime

WORKSPACE = "/home/ubuntu/.openclaw/workspace"

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()

def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default or {}

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_system_stats():
    try:
        disk = run("df -h / | tail -1 | awk '{print $5}'").strip('%')
        disk_free = run("df -h / | tail -1 | awk '{print $4}'")
        load = run("cat /proc/loadavg | awk '{print $1,$2,$3}'")
        uptime = run("cat /proc/uptime | awk '{print $1}'")
        # Gateway status
        gw = "down"
        try:
            subprocess.check_call(["systemctl","is-active","--quiet","openclaw-gateway"])
            gw = "up"
        except:
            pass
        # Git clean?
        git_clean = True
        try:
            status = run(f"git -C {WORKSPACE} status --porcelain")
            git_clean = (status.strip() == "")
        except:
            git_clean = False
        # Updates count (APT)
        updates = 0
        try:
            updates = int(run("apt-get -s upgrade | grep -c ^Inst"))
        except:
            pass
        # Downloads
        downloads_dir = f"{WORKSPACE}/downloads"
        downloads_count = 0
        downloads_gb = 0.0
        if os.path.exists(downloads_dir):
            files = glob.glob(f"{downloads_dir}/*")
            downloads_count = len(files)
            total_bytes = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
            downloads_gb = total_bytes / (1024**3)
        # Memory age days (unused for now)
        memory_age_days = 0
        # Disk history (sparkline): we can return an empty string for now
        disk_history = []
        return {
            "gateway": gw,
            "disk_percent": int(disk) if disk.isdigit() else 0,
            "disk_free": disk_free,
            "load": load,
            "uptime_seconds": int(float(uptime)) if uptime else 0,
            "os": os.uname().sysname,
            "arch": os.uname().machine,
            "updates": updates,
            "git_clean": git_clean,
            "memory_age_days": memory_age_days,
            "disk_history": disk_history,
            "downloads_count": downloads_count,
            "downloads_gb": round(downloads_gb, 2)
        }
    except Exception as e:
        print(f"get_system_stats error: {e}", file=sys.stderr)
        return {}

def parse_active_tasks_lines(lines):
    """Parse active-tasks.md lines into structured dicts."""
    tasks = []
    pattern = r'^- \[([^\]]+)\] (.*?) - (.+?) \(started: ([^,]+), status: ([^)]+)\)$'
    for line in lines:
        line = line.strip()
        if not line.startswith('- ['):
            continue
        m = re.match(pattern, line)
        if m:
            tasks.append({
                'agent': m.group(2).strip(),
                'session_key': m.group(1),
                'goal': m.group(3).strip(),
                'started': m.group(4).strip(),
                'status': m.group(5).strip()
            })
        else:
            tasks.append({
                'agent': 'Unknown',
                'session_key': '',
                'goal': line,
                'started': '',
                'status': 'unknown'
            })
    return tasks[:20]

def get_active_tasks():
    try:
        with open(f"{WORKSPACE}/active-tasks.md") as f:
            return parse_active_tasks_lines(f.readlines())
    except Exception as e:
        print(f"get_active_tasks error: {e}", file=sys.stderr)
        return []

def get_heartbeat():
    hb_path = f"{WORKSPACE}/memory/heartbeat-state.json"
    try:
        with open(hb_path) as f:
            hb = json.load(f)
    except:
        hb = {}
    checks = hb.get('lastChecks', {})
    items = []
    for key, val in checks.items():
        status = val.get('lastStatus', 'ok')
def get_heartbeat():
    """Return heartbeat data in format expected by renderHeartbeat."""
    hb_state_path = f"{WORKSPACE}/memory/heartbeat-state.json"
    hb_checks_path = f"{WORKSPACE}/HEARTBEAT.md"
    state = {}
    try:
        with open(hb_state_path) as f:
            state = json.load(f)
    except:
        state = {}
    # Read checks descriptions from HEARTBEAT.md
    checks_desc = {}
    try:
        with open(hb_checks_path) as f:
            content = f.read()
        # Parse lines like "- **email**: Check inbox (urgent) -> use email"
        for line in content.splitlines():
            if line.startswith('- **'):
                parts = line.split('**')
                if len(parts) >= 3:
                    check_name = parts[1].strip()
                    desc = parts[2].strip().lstrip(': ')
                    checks_desc[check_name] = desc
    except:
        pass

    # Build array of check objects from lastChecks
    last_checks = state.get('lastChecks', {})
    now = int(time.time() * 1000)
    check_items = []
    for check_name, last_ts in last_checks.items():
        last_ms = int(last_ts) * 1000
        ago_min = (now - last_ms) / 60000
        status = 'ok' if ago_min < 120 else 'warn'  # >2h = warn
        check_items.append({
            'check': check_name,
            'last': last_ts,  # original seconds
            'status': status,
            'msg': checks_desc.get(check_name, ''),
            'ago': ago_min
        })

    # Sort by check name for consistent order
    check_items.sort(key=lambda x: x['check'])

    return {
        'state': check_items,
        'checks': checks_desc  # for reference, though frontend may not use
    }
    except:
        return []

def get_agent_outputs(limit=30):
    """Return recent output files (reports, content) with timestamps."""
    outputs = []
    for root, dirs, files in os.walk(f"{WORKSPACE}/reports"):
        for fn in files:
            if fn.endswith('.md'):
                p = os.path.join(root, fn)
                try:
                    st = os.stat(p)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        first = f.readline().strip().lstrip('#').strip()[:80]
                    outputs.append({
                        'ts': int(st.st_mtime * 1000),
                        'title': first or fn,
                        'file': os.path.relpath(p, WORKSPACE),
                        'size': st.st_size
                    })
                except:
                    pass
    for root, dirs, files in os.walk(f"{WORKSPACE}/content"):
        for fn in files:
            if fn.endswith('.md'):
                p = os.path.join(root, fn)
                try:
                    st = os.stat(p)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        first = f.readline().strip().lstrip('#').strip()[:80]
                    outputs.append({
                        'ts': int(st.st_mtime * 1000),
                        'title': first or fn,
                        'file': os.path.relpath(p, WORKSPACE),
                        'size': st.st_size
                    })
                except:
                    pass
    outputs.sort(key=lambda x: x['ts'], reverse=True)
    return outputs[:limit]

def get_latest_commits(limit=10):
    out = run(f"cd {WORKSPACE} && git log --oneline -{limit} --date=relative --pretty=format:'%h %s (%cd)'")
    commits = []
    for line in out.splitlines():
        if line:
            parts = line.split(' ', 1)
            if len(parts)>=2:
                commits.append({"hash": parts[0], "message": parts[1]})
    return commits

def get_cron_jobs():
    try:
        raw = run("openclaw cron list --json")
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start >= 0 and end > start:
            cron_data = json.loads(raw[start:end])
            jobs = []
            for job in cron_data['jobs']:
                st = job['state']
                sched = job['schedule']
                if 'expr' in sched:
                    schedule_str = sched['expr']
                    tz = sched.get('tz','UTC')
                elif 'everyMs' in sched:
                    ms = sched['everyMs']
                    sec = ms/1000
                    if sec < 60:
                        schedule_str = f"every {sec:.0f}s"
                    elif sec < 3600:
                        schedule_str = f"every {sec/60:.0f}m"
                    else:
                        schedule_str = f"every {sec/3600:.0f}h"
                    tz = sched.get('tz','UTC')
                else:
                    schedule_str = 'once'
                    tz = 'UTC'
                jobs.append({
                    'name': job['name'],
                    'schedule': schedule_str,
                    'tz': tz,
                    'enabled': job['enabled'],
                    'last_run': st.get('lastRunAtMs'),
                    'next_run': st.get('nextRunAtMs'),
                    'status': st.get('lastStatus','ok'),
                    'last_error': st.get('lastError','')
                })
            return jobs
    except Exception as e:
        print(f"get_cron_jobs error: {e}", file=sys.stderr)
    return []

def get_sessions():
    try:
        raw = run("openclaw sessions --json")
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start >= 0:
            sessions = json.loads(raw[start:end])
            if isinstance(sessions, dict) and 'sessions' in sessions:
                sessions = sessions['sessions']
            simple = []
            for s in sessions:
                simple.append({
                    "sessionKey": s.get('sessionKey',''),
                    "kinds": s.get('kinds',[]),
                    "lastMsg": s.get('lastMsg','')[:100],
                    "activeSec": s.get('activeSec',0)
                })
            return simple[:20]
    except Exception as e:
        print(f"get_sessions error: {e}", file=sys.stderr)
    return []

def get_content_stats():
    total = 0
    today = 0
    latest_title = ""
    content_dir = f"{WORKSPACE}/content"
    if os.path.exists(content_dir):
        md_files = glob.glob(f"{content_dir}/**/*.md", recursive=True)
        total = len(md_files)
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        for fpath in md_files:
            try:
                mtime = os.path.getmtime(fpath)
                if datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%d') == today_str:
                    today += 1
            except:
                pass
        if md_files:
            latest = max(md_files, key=os.path.getmtime)
            with open(latest, 'r', encoding='utf-8', errors='ignore') as f:
                first = f.readline().strip().lstrip('#').strip()
            latest_title = first
    return {"total": total, "today": today, "latest_title": latest_title}

def get_chat_history(limit=50):
    chat_file = f"{WORKSPACE}/memory/chat.json"
    if os.path.exists(chat_file):
        try:
            with open(chat_file) as f:
                data = json.load(f)
            msgs = data.get('chat', [])
            return msgs[-limit:]
        except:
            pass
    sess_path = "/home/ubuntu/.openclaw/agents/main/sessions/sessions.json"
    if os.path.exists(sess_path):
        try:
            with open(sess_path) as f:
                sessions = json.load(f)
            if sessions:
                latest = sessions[-1]
                msgs = latest.get('messages', [])
                return msgs[-limit:]
        except:
            pass
    return []

def main():
    now = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    out = {
        "generated_at": now,
        "system": get_system_stats(),
        "agents": get_sessions(),
        "research": [],  # TODO: populate from research reports
        "recent_commits": get_latest_commits(10),
        "heartbeat": get_heartbeat(),
        "supervisor_log": get_supervisor_log_tail(30),
        "agent_outputs": get_agent_outputs(30),
        "cron_jobs": get_cron_jobs(),
        "active_tasks": get_active_tasks(),
        "content_stats": get_content_stats(),
        "chat": get_chat_history(50)
    }
    write_json(f"{WORKSPACE}/apps/dashboard/data.json", out)
    print(f"✅ Dashboard data refreshed ({now})")

if __name__ == "__main__":
    main()
