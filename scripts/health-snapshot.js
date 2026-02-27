#!/usr/bin/env node
// quick health snapshot for dashboard /data.json production endpoint
const https = require('https');

const url = process.argv[2] || 'https://openclaw-dashboard-delta.vercel.app/data.json';

https.get(url, { timeout: 5000 }, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      const sys = json.system || {};
      const out = {
        gateway: sys.gateway,
        disk: sys.disk_percent,
        updates: sys.updates,
        git: sys.git_clean,
        memory_age: sys.memory_age_days,
        downloads: { count: sys.downloads_count, gb: sys.downloads_gb },
        generated_at: json.generated_at
      };
      console.log(JSON.stringify(out, null, 2));
      process.exit(0);
    } catch (e) {
      console.error('Parse error:', e.message);
      process.exit(1);
    }
  });
}).on('error', (e) => {
  console.error('Request error:', e.message);
  process.exit(1);
});
