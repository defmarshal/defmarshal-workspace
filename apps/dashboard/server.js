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
 * - GET  /api/tokens      → token usage aggregated per cron job (last 7 days)
 * - POST /api/notify-test → send test push notification
 */

const http  = require('http');
const https = require('https');
const fs    = require('fs');
const json = (res, status, body) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
};
const path  = require('path');
const { spawn, execFile, execFileSync } = require('child_process');

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
const LABEL_OVERRIDES_PATH = path.join(DASHBOARD_DIR, 'session-labels.json');
const CRON_JOBS_JSON = path.join(process.env.HOME, '.openclaw', 'cron', 'jobs.json');
const CRON_RUNS_DIR  = path.join(process.env.HOME, '.openclaw', 'cron', 'runs');

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

// ── Helper: read request body ────────────────────────────────────────────
function readBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); } catch (err) { resolve({}); }
    });
    req.on('error', () => resolve({}));
  });
}

// ── Helper: run a command and capture output ─────────────────────────────
function run(cmd, args = []) {
  return new Promise((resolve) => {
    const proc = spawn(cmd, args, { cwd: WORKSPACE });
    let stdout = '', stderr = '';
    proc.stdout.on('data', d => stdout += d);
    proc.stderr.on('data', d => stderr += d);
    proc.on('close', code => resolve({ ok: code === 0, stdout, stderr, code }));
    proc.on('error', err => resolve({ ok: false, stdout: '', stderr: err.message, code: -1 }));
  });
}

// ── Data cache ────────────────────────────────────────────────────────────
let dataCache = { data: null, timestamp: 0 };
const DATA_CACHE_TTL = 30000; // 30 seconds

// ── Helper: regenerate data.json ─────────────────────────────────────────
async function regenerateData() {
  try {
    const result = await run(path.join(WORKSPACE, 'quick'), ['dash']);
    if (!result.ok) console.warn('regenerateData failed:', result.stderr);
    else dataCache = { data: null, timestamp: Date.now() }; // invalidate cache
  } catch (e) {
    console.warn('regenerateData error:', e.message);
  }
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

// ── Sessions cache ─────────────────────────────────────────────────────────
let sessionsCache = { data: [], timestamp: 0 };
const SESSIONS_CACHE_TTL = 60000; // 60 seconds

function refreshSessionsCache() {
  try {
    const raw = fs.readFileSync(SESSIONS_JSON, 'utf8');
    const sessions = JSON.parse(raw);
    // Load label overrides
    let overrides = {};
    try {
      overrides = JSON.parse(fs.readFileSync(LABEL_OVERRIDES_PATH, 'utf8'));
    } catch (err) {
      // ignore if file missing or invalid
    }
    const list = [];
    for (const [key, val] of Object.entries(sessions)) {
      if (key.includes(':run:')) continue;
      let label = key;
      if (key === 'agent:main:main') {
        label = '💬 Main Session';
      } else if (key.startsWith('agent:main:telegram:')) {
        const parts = key.split(':');
        const type = parts[parts.length-2] || 'unknown';
        const id = parts[parts.length-1] || '';
        label = type === 'direct' ? `👤 Direct:${id}` : type === 'group' ? `👥 Group:${id}` : `📱 Telegram:${id}`;
      } else if (key.startsWith('agent:main:subagent:')) {
        const parts = key.split(':');
        const subId = parts[parts.length-1] || '';
        label = `🤖 Sub-agent:${subId.substring(0,8)}`;
      } else if (key.startsWith('agent:main:cron:')) {
        const valLabel = val.label || '';
        if (valLabel.includes('dev-agent')) label = '👨‍💻 Dev Agent';
        else if (valLabel.includes('content-agent')) label = '📝 Content Agent';
        else if (valLabel.includes('research-agent')) label = '🔬 Research Agent';
        else if (valLabel.includes('game-enhancer')) label = '🎮 Game Enhancer';
        else if (valLabel.includes('vishwakarma')) label = '📐 Vishwakarma';
        else if (valLabel.includes('agni')) label = '🔥 Agni';
        else if (valLabel.includes('evolver')) label = '🧬 Evolver';
        else if (valLabel.startsWith('Cron:')) label = `⏰ ${valLabel.replace(/^Cron: /, '')}`;
        else label = `⏰ Cron`;
      } else if (val.label) {
        label = val.label;
      }
      // Apply override if exists
      if (overrides[key]) {
        label = overrides[key];
      }
      list.push({
        sessionKey: key,
        label,
        updatedAt: val.updatedAt || 0,
        channel: val.channel || 'unknown',
        lastHeartbeatText: val.lastHeartbeatText || ''
      });
    }
    list.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
    sessionsCache = { data: list, timestamp: Date.now() };
  } catch (err) {
    console.error('refreshSessionsCache error:', err);
  }
}

function getAllSessions() {
  return sessionsCache.data;
}

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

// ── Sessions discovery ─────────────────────────────────────────────────────
function getAllSessions() {
  try {
    const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
    const list = [];
    for (const [key, val] of Object.entries(sessions)) {
      // Skip ephemeral cron run sessions (keep only persistent agents)
      if (key.includes(':run:')) continue;
      // Derive a display label from sessionKey
      let label = key;
      if (key === 'agent:main:main') {
        label = '💬 Main Session';
      } else if (key.startsWith('agent:main:telegram:')) {
        const parts = key.split(':');
        const type = parts[parts.length-2] || 'unknown'; // direct or group
        const id = parts[parts.length-1] || '';
        label = type === 'direct' ? `👤 Direct:${id}` : type === 'group' ? `👥 Group:${id}` : `📱 Telegram:${id}`;
      } else if (key.startsWith('agent:main:subagent:')) {
        const parts = key.split(':');
        const subId = parts[parts.length-1] || '';
        label = `🤖 Project:${subId.substring(0,8)}`;
      } else if (key.startsWith('agent:main:cron:')) {
        const valLabel = val.label || '';
        if (valLabel.includes('dev-agent')) label = '👨‍💻 Dev Agent';
        else if (valLabel.includes('content-agent')) label = '📝 Content Agent';
        else if (valLabel.includes('research-agent')) label = '🔬 Research Agent';
        else if (valLabel.includes('game-enhancer')) label = '🎮 Game Enhancer';
        else if (valLabel.includes('vishwakarma')) label = '📐 Vishwakarma';
        else if (valLabel.includes('agni')) label = '🔥 Agni';
        else if (valLabel.includes('evolver')) label = '🧬 Evolver';
        else if (valLabel.startsWith('Cron:')) label = `⏰ ${valLabel.replace(/^Cron: /, '')}`;
        else label = `⏰ Cron`;
      } else if (val.label) {
        label = val.label;
      }
      list.push({
        sessionKey: key,
        label,
        updatedAt: val.updatedAt || 0,
        channel: val.channel || 'unknown',
        lastHeartbeatText: val.lastHeartbeatText || ''
      });
    }
    return list.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
  } catch (err) {
    return [];
  }
}

// ── Chat history helper ────────────────────────────────────────────────────
function getChatHistory(sessionKey) {
  // For direct Telegram chats, always merge across all sessions to preserve history
  if (sessionKey.startsWith('agent:main:telegram:direct:')) {
    const parts = sessionKey.split(':');
    const chatType = parts[3];
    const chatId = parts[4];
    const allSessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
    const matchingKeys = Object.keys(allSessions).filter(k => {
      if (k.includes(':run:')) return false;
      const p = k.split(':');
      if (p.length < 5) return false;
      return p[3] === chatType && p[4] === chatId;
    });
    const allMsgs = [];
    for (const key of matchingKeys) {
      const val = allSessions[key];
      if (!val?.sessionId) continue;
      const sessFile = path.join(SESSIONS_DIR, val.sessionId + '.jsonl');
      if (!fs.existsSync(sessFile)) continue;
      const lines = fs.readFileSync(sessFile, 'utf8').split('\n');
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
          } else { text = String(msg.content || ''); }
          if (!text.trim()) continue;
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
          allMsgs.push({ role, ts: m.timestamp, text });
        } catch (e) {}
      }
    }
    allMsgs.sort((a, b) => new Date(a.ts) - new Date(b.ts));
    return allMsgs.slice(-200);
  }
  try {
    const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
    // If sessionKey not provided or invalid, return empty
    const sessionId = sessions?.[sessionKey]?.sessionId;
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
      } catch (err) {}
    }
    return msgs.slice(-100);
  } catch (err) { return []; }
}

// ── Chat watcher — push notification on new assistant message ──────────────
function startChatWatcher() {
  setInterval(() => {
    // Only check sessions with active SSE clients
    const activeSessions = Array.from(sseClients.keys());
    if (activeSessions.length === 0) return;
    
    for (const sessionKey of activeSessions) {
      const msgs = getChatHistory(sessionKey);
      const assistantCount = msgs.filter(m => m.role === 'assistant').length;
      const prevCount = lastAssistantCounts[sessionKey] || 0;
      if (prevCount > 0 && assistantCount > prevCount) {
        const latest = msgs.filter(m => m.role === 'assistant').pop();
        const preview = (latest?.text || '').slice(0, 100).replace(/\n/g, ' ');
        sendPushToAll({
          title: '🐾 mewmew replied!',
          body: preview || 'New message in ClawDash',
          url: '/?tab=chat',
          tag: 'clawdash-reply',
        }).catch(() => {});
      }
      if (assistantCount !== prevCount) {
        broadcastChat(msgs, sessionKey);
      }
      lastAssistantCounts[sessionKey] = assistantCount;
    }
  }, 2000); // check every 2s
}

// ── aria2 torrent status ──────────────────────────────────────────────────
const ARIA2_URL = 'http://localhost:6800/jsonrpc';
const ARIA2_TOKEN = 'token:openclaw_secret_123';

async function aria2Call(method, params = []) {
  try {
    const body = JSON.stringify({ jsonrpc: '2.0', method, id: '1', params: [ARIA2_TOKEN, ...params] });
    const res = await fetch(ARIA2_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
    const d = await res.json();
    return d.result || [];
  } catch (err) { return []; }
}
function fmtBytes(n) {
  n = parseInt(n) || 0;
  if (n > 1e9) return (n/1e9).toFixed(1) + ' GB';
  if (n > 1e6) return (n/1e6).toFixed(1) + ' MB';
  if (n > 1e3) return (n/1e3).toFixed(1) + ' KB';
  return n + ' B';
}
async function getTorrentStatus() {
  const fields = ['gid','status','totalLength','completedLength','downloadSpeed','uploadSpeed','files','bittorrent','numSeeders','errorMessage'];
  const [active, waiting, stopped] = await Promise.all([
    aria2Call('aria2.tellActive', [fields]),
    aria2Call('aria2.tellWaiting', [0, 10, fields]),
    aria2Call('aria2.tellStopped', [0, 5, fields]),
  ]);
  const fmt = items => items.map(it => {
    const name = it.bittorrent?.info?.name || it.files?.[0]?.path?.split('/').pop() || it.gid;
    const total = parseInt(it.totalLength) || 0;
    const done = parseInt(it.completedLength) || 0;
    const pct = total > 0 ? Math.round(done / total * 100) : 0;
    return {
      gid: it.gid, name, status: it.status, pct,
      speed_dn: fmtBytes(it.downloadSpeed) + '/s',
      speed_up: fmtBytes(it.uploadSpeed) + '/s',
      size: fmtBytes(total), seeders: parseInt(it.numSeeders) || 0,
      error: it.errorMessage || null,
    };
  });
  return { active: fmt(active), waiting: fmt(waiting), stopped: fmt(stopped) };
}

// ── Token usage aggregation ────────────────────────────────────────────────
function getTokenStats() {
  try {
    // Load cron jobs to get id→name mapping
    const cronData = JSON.parse(fs.readFileSync(CRON_JOBS_JSON, 'utf8'));
    const jobs = cronData.jobs || [];
    const idToName = {};
    for (const j of jobs) idToName[j.id] = j.name || j.id;

    const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000; // 7 days ago
    const todayCutoff = new Date();
    todayCutoff.setUTCHours(0, 0, 0, 0);

    // Aggregate from session JSONL files
    // sessions.json maps "agent:main:cron:<cronId>" -> { sessionId }
    const sessionsMap = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));

    // Build cronId -> latest sessionId map
    const cronSessions = {};
    for (const [key, val] of Object.entries(sessionsMap)) {
      const m = key.match(/^agent:main:cron:([^:]+)$/);
      if (m) cronSessions[m[1]] = val.sessionId;
    }

    // Also scan runs/ JSONL files (one per job, contains run records with durationMs)
    // For token data we need the session JSONL files
    const stats = {}; // cronId -> { name, total_in, total_out, total_cache_read, total_cache_write, runs, last_run_ms }

    // Walk all sessions in sessions.json, not just current ones — scan all JSONL files
    // that correspond to cron sessions. The session file may have rotated but we scan all.
    const allKeys = Object.entries(sessionsMap);
    for (const [key, val] of allKeys) {
      const m = key.match(/^agent:main:cron:([^:]+)$/);
      if (!m) continue;
      const cronId = m[1];
      const sessionId = val.sessionId;
      if (!sessionId) continue;
      const sessionFile = path.join(SESSIONS_DIR, sessionId + '.jsonl');
      if (!fs.existsSync(sessionFile)) continue;

      // Read session file and sum usage
      let totalIn = 0, totalOut = 0, totalCacheRead = 0, totalCacheWrite = 0;
      let runCount = 0, lastTs = 0;
      const lines = fs.readFileSync(sessionFile, 'utf8').split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const obj = JSON.parse(line);
          if (obj.type !== 'message') continue;
          const ts = obj.timestamp ? new Date(obj.timestamp).getTime() : 0;
          if (ts < cutoff) continue;
          const usage = obj.message?.usage;
          if (!usage) continue;
          const inp = usage.input || 0;
          const out = usage.output || 0;
          if (inp === 0 && out === 0) continue;
          totalIn += inp;
          totalOut += out;
          totalCacheRead += usage.cacheRead || 0;
          totalCacheWrite += usage.cacheWrite || 0;
          runCount++;
          if (ts > lastTs) lastTs = ts;
        } catch (err) {}
      }
      if (runCount === 0 && totalIn === 0) continue;

      const name = idToName[cronId] || `cron-${cronId.slice(0, 8)}`;
      if (!stats[cronId]) {
        stats[cronId] = { id: cronId, name, total_in: 0, total_out: 0, total_cache_read: 0, total_cache_write: 0, runs: 0, last_run_ms: 0 };
      }
      stats[cronId].total_in += totalIn;
      stats[cronId].total_out += totalOut;
      stats[cronId].total_cache_read += totalCacheRead;
      stats[cronId].total_cache_write += totalCacheWrite;
      stats[cronId].runs += runCount;
      if (lastTs > stats[cronId].last_run_ms) stats[cronId].last_run_ms = lastTs;
    }

    // Also check runs JSONL for more accurate run counts if above is thin
    // (runs dir has one file per job, each line is a run record)
    if (fs.existsSync(CRON_RUNS_DIR)) {
      for (const fname of fs.readdirSync(CRON_RUNS_DIR)) {
        if (!fname.endsWith('.jsonl')) continue;
        const cronId = fname.replace('.jsonl', '');
        if (!stats[cronId]) continue; // only enrich jobs we already have
        const runsFile = path.join(CRON_RUNS_DIR, fname);
        let runCount = 0, lastTs = 0;
        const lines = fs.readFileSync(runsFile, 'utf8').split('\n');
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const obj = JSON.parse(line);
            if (obj.action !== 'finished') continue;
            const ts = obj.ts || 0;
            if (ts < cutoff) continue;
            runCount++;
            if (ts > lastTs) lastTs = ts;
          } catch (err) {}
        }
        // Use max of both counting methods
        if (runCount > stats[cronId].runs) stats[cronId].runs = runCount;
        if (lastTs > stats[cronId].last_run_ms) stats[cronId].last_run_ms = lastTs;
      }
    }

    // Compute today's totals
    let todayTotalIn = 0, todayTotalOut = 0;
    let weekTotalIn = 0, weekTotalOut = 0;
    const rows = Object.values(stats).map(s => {
      const total = s.total_in + s.total_out;
      const avg = s.runs > 0 ? Math.round(total / s.runs) : 0;
      weekTotalIn += s.total_in;
      weekTotalOut += s.total_out;
      return {
        id: s.id,
        name: s.name,
        runs: s.runs,
        total_in: s.total_in,
        total_out: s.total_out,
        total_cache_read: s.total_cache_read,
        total: total,
        avg_tokens: avg,
        last_run_ms: s.last_run_ms,
      };
    });
    rows.sort((a, b) => b.total - a.total);

    return {
      ok: true,
      week: { total_in: weekTotalIn, total_out: weekTotalOut, total: weekTotalIn + weekTotalOut },
      rows,
    };
  } catch (e) {
    return { ok: false, error: e.message, rows: [] };
  }
}

// ── SSE — chat stream ─────────────────────────────────────────────────────
const sseClients = new Map(); // sessionKey -> Set(res)
const lastAssistantCounts = {}; // sessionKey -> assistant message count

function broadcastChat(msgs, sessionKey) {
  const data = 'data: ' + JSON.stringify({ chat: msgs }) + '\n\n';
  const clients = sseClients.get(sessionKey);
  if (!clients) return;
  for (const client of clients) {
    try { client.write(data); } catch { clients.delete(client); }
  }
  if (clients.size === 0) sseClients.delete(sessionKey);
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
  if (pathname === '/api/torrents') {
    const t = await getTorrentStatus();
    cors(res); res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(t));
    return;
  }

  // SSE chat stream
  if (pathname === '/api/chat-stream') {
    const sessionKey = url.searchParams.get('sessionKey');
    if (!sessionKey) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: 'sessionKey required' }));
    }
    // Ensure set exists for this session
    if (!sseClients.has(sessionKey)) sseClients.set(sessionKey, new Set());
    const clients = sseClients.get(sessionKey);
    clients.add(res);

    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    });
    res.write(': connected\n\n');
    // Send current chat immediately for this session
    res.write('data: ' + JSON.stringify({ chat: getChatHistory(sessionKey) }) + '\n\n');
    req.on('close', () => {
      clients.delete(res);
      if (clients.size === 0) sseClients.delete(sessionKey);
    });
    return;
  }

  if (pathname === '/api/notify-test' && req.method === 'POST') {
    await sendPushToAll({ title: '🦾 ClawDash test', body: 'Push notifications are working! nyaa~', url: '/', tag: 'test' });
    return json(res, 200, { ok: true, subs: loadSubs().length });
  }

  // ── Send message ────────────────────────────────────────────────────────
  if (pathname === '/api/send' && req.method === 'POST') {
    const body = await readBody(req);
    const message = (body.message || '').trim();
    if (!message) return json(res, 400, { error: 'message required' });
    const sessionKey = body.sessionKey || 'agent:main:telegram:direct:952170974'; // fallback
    let sessionId = null;
    try {
      const sessions = JSON.parse(fs.readFileSync(SESSIONS_JSON, 'utf8'));
      sessionId = sessions[sessionKey]?.sessionId;
    } catch (err) {}
    if (!sessionId) return json(res, 500, { ok: false, error: 'Could not resolve session ID for key: ' + sessionKey });
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
    const now = Date.now();
    const sessionKey = url.searchParams.get('sessionKey');
    
    // Return cached data if fresh enough
    if (dataCache.data && (now - dataCache.timestamp) < DATA_CACHE_TTL) {
      const data = JSON.parse(JSON.stringify(dataCache.data)); // deep copy
      data.chat = sessionKey ? getChatHistory(sessionKey) : [];
      data.push_enabled = webPush !== null;
      return json(res, 200, data);
    }
    
    // Regenerate if cache is stale or missing
    await regenerateData();
    try {
      const data = JSON.parse(fs.readFileSync(DATA_JSON, 'utf8'));
      dataCache.data = JSON.parse(JSON.stringify(data)); // cache a copy
      data.chat = sessionKey ? getChatHistory(sessionKey) : [];
      data.push_enabled = webPush !== null;
      return json(res, 200, data);
    } catch (e) { return json(res, 500, { error: e.message }); }
  }

  // ── Chat only (fast) ────────────────────────────────────────────────────
  if (pathname === '/api/chat' && req.method === 'GET') {
    const sessionKey = url.searchParams.get('sessionKey');
    if (!sessionKey) return json(res, 400, { error: 'sessionKey required' });
    return json(res, 200, { chat: getChatHistory(sessionKey) });
  }

  // ── List Telegram sessions ───────────────────────────────────────────────
  if (pathname === '/api/sessions' && req.method === 'GET') {
    const sessions = getAllSessions().map(s => {
      const label = s.label;
      return { sessionKey: s.sessionKey, label, updatedAt: s.updatedAt };
    });
    return json(res, 200, { sessions });
  }

  // ── Token usage stats ────────────────────────────────────────────────────
  if (pathname === '/api/tokens' && req.method === 'GET') {
    return json(res, 200, getTokenStats());
  }

  // ── Downloads list ────────────────────────────────────────────────────────
  if (pathname === '/api/downloads-list' && req.method === 'GET') {
    const dlDir = path.join(WORKSPACE, 'downloads');
    try {
      const getFiles = (dir, base='') => {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        let files = [];
        for (const e of entries) {
          const rel = base ? `${base}/${e.name}` : e.name;
          const abs = path.join(dir, e.name);
          if (e.isDirectory()) files = files.concat(getFiles(abs, rel));
          else {
            const st = fs.statSync(abs);
            files.push({ name: e.name, path: rel, size: st.size, mtime: st.mtimeMs });
          }
        }
        return files;
      };
      const files = getFiles(dlDir).sort((a,b) => b.size - a.size);
      const total = files.reduce((s,f) => s+f.size, 0);
      cors(res);
      return json(res, 200, { ok: true, files, total });
    } catch(e) {
      return json(res, 200, { ok: false, files: [], total: 0, error: e.message });
    }
  }


  // ── Projects overview ──────────────────────────────────────────────────────
  if (pathname === '/api/projects' && req.method === 'GET') {
    try {
      const projects = [];
      const projectDirs = [
        { dir: 'games/anime-studio-tycoon', name: 'Anime Studio Tycoon', icon: '🎮' },
        { dir: 'research', name: 'Research Hub', icon: '📚' },
        { dir: 'apps/dashboard', name: 'ClawDash', icon: '📊' },
        { dir: 'docs', name: 'Documentation', icon: '📝' },
        { dir: 'skills', name: 'OpenClaw Skills', icon: '🔧' },
      ];

      for (const p of projectDirs) {
        // Validate path - prevent traversal
        if (!/^[a-z0-9\/_-]+$/i.test(p.dir)) {
          console.warn(`Skipping invalid project dir pattern: ${p.dir}`);
          continue;
        }
        const fullPath = path.join(WORKSPACE, p.dir);
        const normalized = path.normalize(fullPath);
        if (!normalized.startsWith(WORKSPACE)) {
          console.warn(`Skipping path outside workspace: ${p.dir}`);
          continue;
        }
        if (!fs.existsSync(normalized)) continue;

        let lastCommit = null;
        try {
          // Get latest commit that affected this specific project directory
          // Use git -C WORKSPACE log -1 -- <path> to filter by path
          const gitLog = execFileSync('git', ['-C', WORKSPACE, 'log', '-1', '--pretty=format:%H|%s|%cI', '--', p.dir], { encoding: 'utf8', maxBuffer: 1024 * 1024 }).trim();
          if (gitLog) {
            const [hash, message, date] = gitLog.split('|');
            lastCommit = { hash, message, date };
          }
        } catch (e) {
          console.warn(`git log failed for ${p.dir}:`, e.message);
        }

        let status = 'idle';
        try {
          const gitStatus = execFileSync('git', ['-C', normalized, 'status', '--porcelain'], { encoding: 'utf8', maxBuffer: 1024 * 1024 }).trim();
          if (gitStatus) status = 'active';
        } catch (e) {
          console.warn(`git status failed for ${p.dir}:`, e.message);
        }

        let description = '';
        try {
          const readmePath = path.join(normalized, 'README.md');
          if (fs.existsSync(readmePath)) {
            const readme = fs.readFileSync(readmePath, 'utf8');
            const firstLine = readme.split('\n')[0].trim();
            description = firstLine.replace(/^#+\s*/, '').replace(/<[^>]*>/g, '').trim();
          }
        } catch (e) {
          console.warn(`README read failed for ${p.dir}:`, e.message);
        }

        projects.push({
          name: p.name,
          icon: p.icon,
          description: description || `${p.name} project`,
          path: p.dir,
          status,
          lastCommit,
        });
      }

      cors(res);
      return json(res, 200, { ok: true, projects });
    } catch (e) {
      console.error('Projects API error:', e.message);
      return json(res, 500, { ok: false, error: e.message });
    }
  }

  // ── Download a file ───────────────────────────────────────────────────────
  if (pathname.startsWith('/api/download/') && req.method === 'GET') {
    const rel = decodeURIComponent(pathname.slice('/api/download/'.length));
    if (rel.includes('..')) return json(res, 400, { error: 'invalid path' });
    const abs = path.join(WORKSPACE, 'downloads', rel);
    if (!abs.startsWith(path.join(WORKSPACE, 'downloads'))) return json(res, 403, { error: 'forbidden' });
    try {
      const st = fs.statSync(abs);
      const fname = path.basename(abs);
      cors(res);
      res.writeHead(200, {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename*=UTF-8''${encodeURIComponent(fname)}`,
        'Content-Length': st.size,
      });
      fs.createReadStream(abs).pipe(res);
    } catch(e) {
      return json(res, 404, { error: 'not found' });
    }
    return;
  }

  // ── Delete a download ─────────────────────────────────────────────────────
  if (pathname.startsWith('/api/download/') && req.method === 'DELETE') {
    const rel = decodeURIComponent(pathname.slice('/api/download/'.length));
    if (rel.includes('..')) return json(res, 400, { error: 'invalid path' });
    const abs = path.join(WORKSPACE, 'downloads', rel);
    if (!abs.startsWith(path.join(WORKSPACE, 'downloads'))) return json(res, 403, { error: 'forbidden' });
    try {
      fs.rmSync(abs, { recursive: true, force: true });
      // Remove parent dir if empty
      const parent = path.dirname(abs);
      if (parent !== path.join(WORKSPACE, 'downloads')) {
        const remaining = fs.readdirSync(parent);
        if (remaining.length === 0) fs.rmdirSync(parent);
      }
      cors(res);
      return json(res, 200, { ok: true });
    } catch(e) {
      return json(res, 500, { error: e.message });
    }
  }



  // ── Download all as ZIP ────────────────────────────────────────────────────
  if (pathname === '/api/downloads-zip' && req.method === 'GET') {
    const downloadsDir = path.join(WORKSPACE, 'downloads');
    if (!fs.existsSync(downloadsDir)) {
      return json(res, 404, { error: 'No downloads' });
    }
    try {
      const files = fs.readdirSync(downloadsDir);
      if (files.length === 0) {
        return json(res, 404, { error: 'No downloads to zip' });
      }
    } catch(e) {
      return json(res, 500, { error: e.message });
    }
    cors(res);
    const zipName = `mewdash-downloads-${new Date().toISOString().slice(0,10)}.zip`;
    res.writeHead(200, {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${zipName}"`,
    });
    const zip = spawn('zip', ['-r', '-', '.'], { cwd: downloadsDir, stdio: ['ignore', 'pipe', 'inherit'] });
    zip.stdout.pipe(res);
    zip.on('error', err => {
      console.error('zip spawn error:', err);
      if (!res.headersSent) {
        res.writeHead(500);
        res.end(JSON.stringify({ error: 'zip failed' }));
      }
    });
    zip.on('close', code => {
      if (code !== 0) {
        console.error(`zip exited with code ${code}`);
      }
    });
    return;
  }

  // ── Agent Control ─────────────────────────────────────────────────────────────
  if (pathname === '/api/cron/run' && req.method === 'POST') {
    console.log('[CRON RUN]', new Date().toISOString());
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { cronId } = JSON.parse(body);
        if (!cronId) return json(res, 400, { error: 'cronId required' });
        console.log('[CRON RUN] Executing cron:', cronId);
        execFile('/home/ubuntu/.npm-global/bin/openclaw', ['cron','run', cronId], { timeout: 120000 }, (err, stdout, stderr) => {
          if (err) {
            console.error('[CRON RUN] Error:', err.message, stderr);
            return json(res, 500, { error: err.message, stderr, stdout });
          }
          console.log('[CRON RUN] Success:', stdout.slice(0, 200));
          json(res, 200, { ok: true, output: stdout, stderr });
        });
      } catch (e) {
        console.error('[CRON RUN] Parse error:', e.message);
        json(res, 500, { error: e.message });
      }
    });
    req.on('error', (e) => {
      console.error('[CRON RUN] Request error:', e.message);
    });
    return;
  }

  if (pathname === '/api/session/stop' && req.method === 'POST') {
    console.log('[SESSION STOP]', new Date().toISOString());
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { sessionKey } = JSON.parse(body);
        if (!sessionKey) return json(res, 400, { error: 'sessionKey required' });
        execFile('/home/ubuntu/.npm-global/bin/openclaw', ['sessions','stop', sessionKey], (err, stdout, stderr) => {
          if (err) return json(res, 500, { error: err.message, stderr });
          json(res, 200, { ok: true, output: stdout });
        });
      } catch (e) {
        json(res, 500, { error: e.message });
      }
    });
    return;
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

// ── Error handling ───────────────────────────────────────────────────────
process.on('uncaughtException', (err) => {
  console.error('[FATAL] Uncaught Exception:', err.message);
  console.error(err.stack);
});
process.on('unhandledRejection', (reason, promise) => {
  console.error('[FATAL] Unhandled Rejection at:', promise, 'reason:', reason);
});

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
// Initialize sessions cache and refresh periodically
refreshSessionsCache();
setInterval(refreshSessionsCache, SESSIONS_CACHE_TTL);
console.log('📦 Sessions cache initialized (refresh every 60s)');
// ── aria2 torrent status ──────────────────────────────────────────────────
