#!/usr/bin/env node
/**
 * ClawDash Backend Server
 * - Serves the PWA from apps/dashboard/
 * - POST /api/send        → sends message to mewmew via openclaw agent
 * - POST /api/quick       → runs ./quick <cmd> safely
 * - GET  /api/data        → returns latest data.json (regenerated on demand)
 * - GET  /api/chat        → returns chat messages from current telegram session
 * - GET  /api/vapid-key   → returns VAPID public key for push subscription
 * - POST /api/subscribe   → saves push subscription
 * - POST /api/notify-test → send test push notification
 */

const http  = require('http');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const { spawn, execFile } = require('child_process');

const PORT       = 3001;
const HTTPS_PORT = 3443;
const HOST       = '0.0.0.0';
const WORKSPACE     = path.join(process.env.HOME, '.openclaw', 'workspace');
const DASHBOARD_DIR = path.join(WORKSPACE, 'apps', 'dashboard');
const DATA_JSON     = path.join(DASHBOARD_DIR, 'data.json');
const SESSIONS_JSON = path.join(process.env.HOME, '.openclaw', 'agents', 'main', 'sessions', 'sessions.json');
const SESSIONS_DIR  = path.join(process.env.HOME, '.openclaw', 'agents', 'main', 'sessions');
const CERT_PATH     = path.join(DASHBOARD_DIR, 'tls.crt');
const KEY_PATH      = path.join(DASHBOARD_DIR, 'tls.key');
const VAPID_PATH    = path.join(DASHBOARD_DIR, 'vapid.json');
const SUBS_PATH     = path.join(DASHBOARD_DIR, 'push-subscriptions.json');

// ── VAPID / web-push setup ─────────────────────────────────────────────────
let webPush = null;
let vapid = null;
try {
  webPush = require(path.join(WORKSPACE, 'node_modules', 'web-push'));
  vapid = JSON.parse(fs.readFileSync(VAPID_PATH, 'utf8'));
  webPush.setVapidDetails(vapid.subject, vapid.publicKey, vapid.privateKey);
  console.log('🔔 Push notifications ready');
} catch (e) {
  console.warn('⚠️  web-push not available:', e.message);
}

// ── Subscription store ────────────────────────────────────────────────────
function loadSubs() {
  try { return JSON.parse(fs.readFileSync(SUBS_PATH, 'utf8')); } catch { return []; }
}
function saveSubs(subs) {
  fs.writeFileSync(SUBS_PATH, JSON.stringify(subs, null, 2));
}
function addSub(sub) {
  const subs = loadSubs();
  const exists = subs.some(s => s.endpoint === sub.endpoint);
  if (!exists) { subs.push(sub); saveSubs(subs); }
}

async function sendPushToAll(payload) {
  if (!webPush) return;
  const subs = loadSubs();
  if (!subs.length) return;
  const dead = [];
  for (const sub of subs) {
    try {
      await webPush.sendNotification(sub, JSON.stringify(payload));
    } catch (e) {
      if (e.statusCode === 410 || e.statusCode === 404) dead.push(sub.endpoint);
      else console.warn('push failed:', e.message);
    }
  }
  if (dead.length) saveSubs(subs.filter(s => !dead.includes(s.endpoint)));
}

// ── Allowed quick commands ────────────────────────────────────────────────
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
  '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.ico': 'image/x-icon', '.webp': 'image/webp',
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
    req.on('data', d => { body += d; if (body.length > 65536) reject(new Error('body too large')); });
    req.on('end', () => { try { resolve(JSON.parse(body)); } catch { resolve({}); } });
    req.on('error', reject);
  });
}
function run(cmd, args, opts = {}) {
  return new Promise((resolve) => {
    execFile(cmd, args, { timeout: 30000, cwd: WORKSPACE, ...opts }, (err, stdout, stderr) => {
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
    for (const line of fs.readFileSync(sessionFile, 'utf8').split('\n')) {
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
        } else { text = String(msg.content || ''); }
        if (role === 'user' && text.includes('Conversation info')) {
          const end = text.indexOf('```\n\n');
          if (end >= 0) text = text.slice(end + 5).trim();
        }
        if (!text.trim()) continue;
        // Filter out system/meta messages
        if (text === 'HEARTBEAT_OK') continue;
        if (text.startsWith('[System Message]')) continue;
        if (text.startsWith('Read HEARTBEAT')) continue;
        if (text.startsWith('Pre-compaction memory flush')) continue;
        if (text.startsWith('NO_REPLY')) continue;
        if (text.includes('Conversation info (untrusted metadata)')) continue;
        if (text.startsWith('Continue') && text.length < 20) continue;
        if (text.startsWith('Continueeee')) continue;
        if (role === 'assistant' && text === 'NO_REPLY') continue;
        if (text.length < 2) continue;
        msgs.push({ role, ts: m.timestamp, text });
      } catch {}
    }
    return msgs.slice(-100);
  } catch { return []; }
}

// ── Chat watcher — push notification on new assistant message ──────────────
let lastAssistantMsgCount = 0;
function startChatWatcher() {
  setInterval(() => {
    const msgs = getChatHistory();
    const assistantCount = msgs.filter(m => m.role === 'assistant').length;
    if (lastAssistantMsgCount > 0 && assistantCount > lastAssistantMsgCount) {
      const latest = msgs.filter(m => m.role === 'assistant').pop();
      const preview = (latest?.text || '').slice(0, 100).replace(/\n/g, ' ');
      sendPushToAll({
        title: '🐾 mewmew replied!',
        body: preview || 'New message in ClawDash',
        url: '/?tab=chat',
        tag: 'clawdash-reply',
      }).catch(() => {});
    }
    lastAssistantMsgCount = assistantCount;
  }, 5000); // check every 5s
}

// ── Request handler ───────────────────────────────────────────────────────
const handler = async (req, res) => {
  const url = new URL(req.url, `https://${req.headers.host}`);
  const pathname = url.pathname;

  if (req.method === 'OPTIONS') { cors(res); res.writeHead(204); res.end(); return; }

  // ── VAPID public key ────────────────────────────────────────────────────
  if (pathname === '/api/vapid-key' && req.method === 'GET') {
    return json(res, 200, { publicKey: vapid?.publicKey || null });
  }

  // ── Save push subscription ──────────────────────────────────────────────
  if (pathname === '/api/subscribe' && req.method === 'POST') {
    const body = await readBody(req);
    if (!body.endpoint) return json(res, 400, { error: 'invalid subscription' });
    addSub(body);
    console.log('New push subscriber:', body.endpoint.slice(0, 60) + '…');
    return json(res, 200, { ok: true });
  }

  // ── Test push notification ──────────────────────────────────────────────
  if (pathname === '/api/notify-test' && req.method === 'POST') {
    await sendPushToAll({ title: '🦾 ClawDash test', body: 'Push notifications are working! nyaa~', url: '/', tag: 'test' });
    return json(res, 200, { ok: true, subs: loadSubs().length });
  }

  // ── Send message ────────────────────────────────────────────────────────
  if (pathname === '/api/send' && req.method === 'POST') {
    const body = await readBody(req);
    const message = (body.message || '').trim();
    if (!message) return json(res, 400, { error: 'message required' });
    let sessionId = null;
    try {
      const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
      sessionId = sessions['agent:main:telegram:direct:952170974']?.sessionId;
    } catch {}
    if (!sessionId) return json(res, 500, { ok: false, error: 'Could not resolve session ID' });
    const proc = spawn('openclaw', ['agent', '--session-id', sessionId, '--message', message, '--deliver'],
      { detached: true, stdio: 'ignore', cwd: WORKSPACE });
    proc.unref();
    return json(res, 200, { ok: true, output: 'Message queued — reply coming via Telegram' });
  }

  // ── Quick command ───────────────────────────────────────────────────────
  if (pathname === '/api/quick' && req.method === 'POST') {
    const body = await readBody(req);
    const parts = (body.cmd || '').trim().split(/\s+/);
    const cmd = parts[0], args = parts.slice(1);
    if (!ALLOWED_QUICK.has(cmd))
      return json(res, 403, { error: `command '${cmd}' not allowed` });
    const result = await run(path.join(WORKSPACE, 'quick'), [cmd, ...args]);
    return json(res, 200, { ok: result.ok, output: (result.stdout + result.stderr).trim() });
  }

  // ── Data (live) ─────────────────────────────────────────────────────────
  if (pathname === '/api/data' && req.method === 'GET') {
    await regenerateData();
    try {
      const data = JSON.parse(fs.readFileSync(DATA_JSON, 'utf8'));
      data.chat = getChatHistory();
      data.push_enabled = webPush !== null;
      return json(res, 200, data);
    } catch (e) { return json(res, 500, { error: e.message }); }
  }

  // ── Chat only (fast) ────────────────────────────────────────────────────
  if (pathname === '/api/chat' && req.method === 'GET') {
    return json(res, 200, { chat: getChatHistory() });
  }

  // ── Static files ─────────────────────────────────────────────────────────
  let filePath = pathname === '/' ? '/index.html' : pathname;
  filePath = path.join(DASHBOARD_DIR, filePath.replace(/\.\./g, ''));
  if (!filePath.startsWith(DASHBOARD_DIR)) { res.writeHead(403); res.end('Forbidden'); return; }
  const ext = path.extname(filePath);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      fs.readFile(path.join(DASHBOARD_DIR, 'index.html'), (e2, d2) => {
        if (e2) { res.writeHead(404); res.end('Not found'); return; }
        cors(res); res.writeHead(200, { 'Content-Type': 'text/html' }); res.end(d2);
      });
      return;
    }
    cors(res);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
};

// ── Servers ───────────────────────────────────────────────────────────────
const server = http.createServer(handler);
server.listen(PORT, HOST, () => {
  console.log(`🦾 ClawDash HTTP  → http://localhost:${PORT}`);
  console.log(`   Tailscale IP   → http://100.108.208.45:${PORT}`);
});

try {
  const tlsOpts = { cert: fs.readFileSync(CERT_PATH), key: fs.readFileSync(KEY_PATH) };
  const httpsServer = https.createServer(tlsOpts, handler);
  httpsServer.listen(HTTPS_PORT, HOST, () => {
    console.log(`🔒 ClawDash HTTPS → https://instance-20260207-2229.tail2dd22b.ts.net:${HTTPS_PORT}`);
  });
} catch (e) {
  console.warn('⚠️  HTTPS not available:', e.message);
}

startChatWatcher();
console.log('👀 Chat watcher running — push on new reply');
