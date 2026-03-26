#!/usr/bin/env python3
"""
OpenClaw MCP Server - Exposes system health and agent tools via Model Context Protocol.
Run: python3 agents/mcp-openclaw-server.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="OpenClaw MCP Server", version="0.1.0")

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
OPENCLAW = "/home/ubuntu/.npm-global/bin/openclaw"

def run_cmd(cmd: List[str], timeout: int = 30) -> tuple[str, str, int]:
    """Run command and return stdout, stderr, exit code."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Timeout after {timeout}s", 1
    except Exception as e:
        return "", str(e), 1

def get_system_status() -> Dict[str, Any]:
    """Get overall system health snapshot."""
    # Disk usage
    disk_out, _, _ = run_cmd(["df", "-h", "."])
    disk_line = disk_out.split()[11] if len(disk_out.split()) > 11 else "N/A"
    
    # Gateway status
    gw_out, _, gw_rc = run_cmd([OPENCLAW, "gateway", "status"])
    gateway_up = gw_rc == 0 and "running" in gw_out.lower()
    
    # Cron summary
    cron_out, _, _ = run_cmd([OPENCLAW, "cron", "list", "--json"])
    cron_healthy = True
    try:
        cron_data = json.loads(cron_out)
        failures = [j for j in cron_data.get("jobs", []) if j.get("state", {}).get("lastStatus") != "ok"]
        cron_healthy = len(failures) == 0
    except:
        cron_healthy = False
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "disk_usage": disk_line,
        "gateway": "healthy" if gateway_up else "down",
        "cron_healthy": cron_healthy,
        "uptime": run_cmd(["uptime"])[0].strip() if sys.platform != "win32" else "N/A"
    }

def list_agents() -> Dict[str, Any]:
    """List active OpenClaw sessions/agents."""
    out, _, rc = run_cmd([OPENCLAW, "sessions", "list", "--activeMinutes", "5", "--json"])
    if rc != 0:
        return {"error": "failed to list sessions", "sessions": []}
    try:
        data = json.loads(out)
        sessions = data.get("sessions", [])
        summary = [
            {
                "agentId": s.get("agentId"),
                "sessionKey": s.get("sessionKey", "")[:8],
                "updatedAt": s.get("updatedAtMs")
            }
            for s in sessions
        ]
        return {"count": len(sessions), "sessions": summary}
    except Exception as e:
        return {"error": str(e), "sessions": []}

def get_cron_health() -> Dict[str, Any]:
    """Get detailed cron job health."""
    out, _, rc = run_cmd([OPENCLAW, "cron", "list", "--json"])
    if rc != 0:
        return {"error": "failed to fetch cron jobs"}
    try:
        data = json.loads(out)
        jobs = data.get("jobs", [])
        failures = []
        for j in jobs:
            state = j.get("state", {})
            if state.get("lastStatus") != "ok" or state.get("consecutiveErrors", 0) > 2:
                failures.append({
                    "name": j.get("name"),
                    "lastStatus": state.get("lastStatus"),
                    "errors": state.get("consecutiveErrors"),
                    "lastRun": state.get("lastRunAtMs")
                })
        return {
            "total": len(jobs),
            "healthy": len(jobs) - len(failures),
            "failures": failures
        }
    except Exception as e:
        return {"error": str(e)}

def trigger_agent(agent_name: str) -> Dict[str, Any]:
    """Trigger a one-off agent run (via cron payload simulation)."""
    # Map agent name to actual script
    agent_scripts = {
        "research": "./agents/research-cycle.sh",
        "content": "./agents/content-cycle.sh",
        "dev": "./agents/dev-cycle.sh",
        "code-gardener": "python3 agents/code-gardener.py",
        "seed-gatherer": "python3 agents/seed-gatherer.py"
    }
    if agent_name not in agent_scripts:
        return {"error": f"Unknown agent: {agent_name}. Available: {list(agent_scripts.keys())}"}
    
    cmd = ["bash", "-c", f"cd {WORKSPACE} && {agent_scripts[agent_name]}"]
    stdout, stderr, rc = run_cmd(cmd, timeout=10)
    return {
        "agent": agent_name,
        "exit_code": rc,
        "stdout": stdout[:500],
        "stderr": stderr[:500] if stderr else None
    }

def get_recent_logs(agent: str = None, lines: int = 20) -> Dict[str, Any]:
    """Get recent log tail for an agent or general system."""
    log_map = {
        "agent-manager": "memory/agent-manager.log",
        "supervisor": "memory/supervisor.log",
        "code-gardener": "memory/code-gardener.log",
        "research": "memory/research-agent.log",
        "content": "memory/content-agent.log",
        "dev": "memory/dev-agent.log",
        "gateway": "/tmp/openclaw/openclaw.log"
    }
    if agent and agent not in log_map:
        return {"error": f"Unknown agent log: {agent}. Available: {list(log_map.keys())}"}
    
    log_file = log_map[agent] if agent else "memory/agent-manager.log"
    if not Path(log_file).exists():
        return {"error": f"Log file not found: {log_file}"}
    
    # Tail using system command
    cmd = ["tail", "-n", str(lines), log_file]
    stdout, _, _ = run_cmd(cmd)
    return {"log": stdout, "file": log_file}

def get_unprocessed_seeds(limit: int = 10) -> Dict[str, Any]:
    """List seeds that haven't been processed yet."""
    seeds_file = WORKSPACE / "memory" / "seeds.jsonl"
    processed_file = WORKSPACE / "memory" / "processed_seeds.jsonl"
    if not seeds_file.exists():
        return {"error": "seeds.jsonl not found"}
    
    # Load processed IDs
    processed = set()
    if processed_file.exists():
        with open(processed_file) as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    processed.add(data.get("id"))
                except:
                    continue
    
    # Load unprocessed seeds
    unprocessed = []
    with open(seeds_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                seed = json.loads(line)
                if seed.get("id") not in processed:
                    unprocessed.append({
                        "id": seed.get("id"),
                        "title": seed.get("title"),
                        "source": seed.get("source"),
                        "ts": seed.get("ts")
                    })
                    if len(unprocessed) >= limit:
                        break
            except:
                continue
    
    return {
        "total_unprocessed": len(unprocessed) if len(unprocessed) < limit else "many",
        "seeds": unprocessed
    }

# MCP JSON-RPC endpoint
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Handle MCP JSON-RPC requests."""
    data = await request.json()
    method = data.get("method")
    params = data.get("params", {})
    request_id = data.get("id")
    
    # Route to tools
    result = None
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_system_status":
            result = get_system_status()
        elif tool_name == "list_agents":
            result = list_agents()
        elif tool_name == "get_cron_health":
            result = get_cron_health()
        elif tool_name == "trigger_agent":
            result = trigger_agent(arguments.get("agent_name"))
        elif tool_name == "get_recent_logs":
            result = get_recent_logs(
                agent=arguments.get("agent"),
                lines=arguments.get("lines", 20)
            )
        elif tool_name == "get_unprocessed_seeds":
            result = get_unprocessed_seeds(limit=arguments.get("limit", 10))
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
    elif method == "tools/list":
        # Return list of available tools
        result = {
            "tools": [
                {
                    "name": "get_system_status",
                    "description": "Get system health snapshot (disk, gateway, cron status, uptime)",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "list_agents",
                    "description": "List active OpenClaw sessions/agents (last 5 min)",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "get_cron_health",
                    "description": "Get detailed cron job health, list failures",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "trigger_agent",
                    "description": "Trigger a one-off agent run (research, content, dev, code-gardener, seed-gatherer)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "agent_name": {"type": "string", "enum": ["research", "content", "dev", "code-gardener", "seed-gatherer"]}
                        },
                        "required": ["agent_name"]
                    }
                },
                {
                    "name": "get_recent_logs",
                    "description": "Tail logs for an agent or system",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "agent": {"type": "string", "enum": ["agent-manager", "supervisor", "code-gardener", "research", "content", "dev", "gateway"]},
                            "lines": {"type": "integer", "default": 20}
                        }
                    }
                },
                {
                    "name": "get_unprocessed_seeds",
                    "description": "List research seeds that haven't been processed yet",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "default": 10}
                        }
                    }
                }
            ]
        }
    else:
        result = {"error": f"Unsupported method: {method}"}
    
    return JSONResponse({
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    })

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw MCP Server")
    parser.add_argument("--port", type=int, default=3001, help="Port to listen on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    args = parser.parse_args()
    
    print(f"Starting OpenClaw MCP Server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
