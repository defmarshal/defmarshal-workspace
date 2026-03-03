const fs = require('fs');
const path = '/home/ubuntu/.openclaw/workspace/apps/dashboard/data.json';
try {
  const raw = fs.readFileSync(path, 'utf8');
  const data = JSON.parse(raw);
  console.log('data.json loaded OK, fields:', Object.keys(data));
} catch (e) {
  console.error('Failed to load data.json:', e && e.stack ? e.stack : e);
  process.exit(1);
}