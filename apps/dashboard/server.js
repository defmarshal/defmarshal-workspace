#!/usr/bin/env node
/**
 * ClawDash Backend Server
 * - Serves the PWA from apps/dashboard/
 * - POST /api/send   → sends message to mewmew via openclaw agent
 * - POST /api/quick  → runs ./quick <cmd> safely
 * - GET  /api/data   → returns latest data.json (regenerated on demand)
 * - GET  /api/chat   → returns chat messages from current telegram session
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { spawn, execFile } = require('child_process');

const PORT = 3001;
const HTTPS_PORT = 3443;
const HOST = '0.0.0.0';
const WORKSPACE = path.join(process.env.HOME, '.openclaw', 'workspace');
const DASHBOARD_DIR = path.join(WORKSPACE, 'apps', 'dashboard');
const DATA_JSON = path.join(DASHBOARD_DIR, 'data.json');
const SESSIONS_JSON = path.join(process.env.HOME, '.openclaw', 'agents', 'main', 'sessions', 'sessions.json');
const SESSIONS_DIR = path.join(process.env.HOME, '.openclaw', 'agents', 'main', 'sessions');
const CERT_PATH = path.join(DASHBOARD_DIR, 'tls.crt');
const KEY_PATH  = path.join(DASHBOARD_DIR, 'tls.key');

// Allowed quick commands (whitelist for safety)
const ALLOWED_QUICK = new Set([
  'health', 'status', 'summary', 'dash', 'agents-summary', 'log-tail',
  'top-commits', 'mem', 'memory-status', 'memory-dirty', 'memory-stats',
  'heartbeat-state', 'hygiene', 'cron', 'cron-status', 'cron-failures',
  'gateway-status', 'gateway-info', 'daemons', 'agent-status', 'dev-log',
  'today', 'git-status', 'git-today', 'git-summary', 'git-last',
  'downloads', 'torrent-status', 'updates-check', 'voyage-status',
  'orphan-check', 'checkpoints', 'phase', 'reports', 'digest',
  'health-snapshot', 'vercel-status', 'validate', 'verify',
  'supervisor-logs', 'meta-logs', 'meta-report',
]);

const MIME = {
  '.html': 'text/html',
  '.js':   'application/javascript',
  '.css':  'text/css',
  '.json': 'application/json',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.ico':  'image/x-icon',
  '.webp': 'image/webp',
  '.webmanifest': 'application/manifest+json',
};

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function json(res, code, obj) {
  cors(res);
  res.writeHead(code, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', d => { body += d; if (body.length > 8192) reject(new Error('body too large')); });
    req.on('end', () => { try { resolve(JSON.parse(body)); } catch { resolve({}); } });
    req.on('error', reject);
  });
}

function run(cmd, args, opts = {}) {
  return new Promise((resolve) => {
    const proc = execFile(cmd, args, { timeout: 30000, cwd: WORKSPACE, ...opts }, (err, stdout, stderr) => {
      resolve({ ok: !err, stdout: stdout || '', stderr: stderr || '', code: err?.code || 0 });
    });
  });
}

async function regenerateData() {
  return run('bash', [path.join(WORKSPACE, 'scripts', 'generate-dashboard-data.sh')]);
}

function getChatHistory() {
  try {
    const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
    const sessionId = sessions['agent:main:telegram:direct:952170974']?.sessionId;
    if (!sessionId) return [];
    const sessionFile = path.join(SESSIONS_DIR, sessionId + '.jsonl');
    if (!fs.existsSync(sessionFile)) return [];

    const msgs = [];
    const lines = fs.readFileSync(sessionFile, 'utf8').split('\n');
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const m = JSON.parse(line);
        if (m.type !== 'message') continue;
        const msg = m.message;
        const role = msg.role;
        if (!['user', 'assistant'].includes(role)) continue;
        let text = '';
        if (Array.isArray(msg.content)) {
          text = msg.content.filter(c => c.type === 'text').map(c => c.text).join(' ');
        } else {
          text = String(msg.content || '');
        }
        // strip telegram metadata header
        if (role === 'user' && text.includes('Conversation info')) {
          const end = text.indexOf('```\n\n');
          if (end >= 0) text = text.slice(end + 5).trim();
        }
        // skip system/heartbeat messages
        if (!text.trim()) continue;
        if (text.startsWith('[System Message]') || text.startsWith('Read HEARTBEAT') || text === 'HEARTBEAT_OK') continue;
        msgs.push({ role, ts: m.timestamp, text });
      } catch {}
    }
    return msgs.slice(-100);
  } catch (e) {
    return [];
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  if (req.method === 'OPTIONS') { cors(res); res.writeHead(204); res.end(); return; }

  // ── API: send message ──────────────────────────────────────────────────────
  if (pathname === '/api/send' && req.method === 'POST') {
    const body = await readBody(req);
    const message = (body.message || '').trim();
    if (!message) return json(res, 400, { error: 'message required' });

    // Look up session ID dynamically
    let sessionId = null;
    try {
      const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
      sessionId = sessions['agent:main:telegram:direct:952170974']?.sessionId;
    } catch {}

    if (!sessionId) {
      return json(res, 500, { ok: false, error: 'Could not resolve session ID' });
    }

    // Fire agent turn detached (background) — returns immediately, reply arrives in Telegram
    const proc = require('child_process').spawn(
      'openclaw',
      ['agent', '--session-id', sessionId, '--message', message, '--deliver'],
      { detached: true, stdio: 'ignore', cwd: WORKSPACE }
    );
    proc.unref();

    return json(res, 200, { ok: true, output: 'Message queued — reply coming via Telegram' });
  }

  // ── API: run quick command ─────────────────────────────────────────────────
  if (pathname === '/api/quick' && req.method === 'POST') {
    const body = await readBody(req);
    const cmd = (body.cmd || '').trim().split(/\s+/)[0];
    const args = (body.cmd || '').trim().split(/\s+/).slice(1);
    if (!ALLOWED_QUICK.has(cmd)) {
      return json(res, 403, { error: `command '${cmd}' not allowed. Allowed: ${[...ALLOWED_QUICK].join(', ')}` });
    }
    const result = await run(path.join(WORKSPACE, 'quick'), [cmd, ...args]);
    return json(res, 200, {
      ok: result.ok,
      output: (result.stdout + result.stderr).trim(),
    });
  }

  // ── API: refresh + return data.json ───────────────────────────────────────
  if (pathname === '/api/data' && req.method === 'GET') {
    await regenerateData();
    try {
      const data = JSON.parse(fs.readFileSync(DATA_JSON, 'utf8'));
      data.chat = getChatHistory();
      return json(res, 200, data);
    } catch (e) {
      return json(res, 500, { error: e.message });
    }
  }

  // ── API: chat only (fast, no regen) ───────────────────────────────────────
  if (pathname === '/api/chat' && req.method === 'GET') {
    return json(res, 200, { chat: getChatHistory() });
  }

  // ── Static files ──────────────────────────────────────────────────────────
  let filePath = pathname === '/' ? '/index.html' : pathname;
  filePath = path.join(DASHBOARD_DIR, filePath.replace(/\.\./g, ''));
  if (!filePath.startsWith(DASHBOARD_DIR)) { res.writeHead(403); res.end('Forbidden'); return; }

  const ext = path.extname(filePath);
  const mime = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // fallback to index.html for PWA routing
      fs.readFile(path.join(DASHBOARD_DIR, 'index.html'), (err2, d2) => {
        if (err2) { res.writeHead(404); res.end('Not found'); return; }
        cors(res);
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(d2);
      });
      return;
    }
    cors(res);
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
});

server.listen(PORT, HOST, () => {
  console.log(`🦾 ClawDash HTTP  → http://localhost:${PORT}`);
  console.log(`   Tailscale IP   → http://100.108.208.45:${PORT}`);
});

// HTTPS server for PWA install (Chrome on Android requires HTTPS)
try {
  const tlsOpts = {
    cert: fs.readFileSync(CERT_PATH),
    key:  fs.readFileSync(KEY_PATH),
  };
  const httpsServer = https.createServer(tlsOpts, server.listeners('request')[0]);
  httpsServer.listen(HTTPS_PORT, HOST, () => {
    console.log(`🔒 ClawDash HTTPS → https://instance-20260207-2229.tail2dd22b.ts.net:${HTTPS_PORT}`);
    console.log(`   (use HTTPS URL for PWA install on Android Chrome)`);
  });
} catch (e) {
  console.warn('⚠️  HTTPS not available:', e.message);
}
