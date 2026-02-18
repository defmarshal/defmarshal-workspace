const http = require('http');
const fs = require('fs');
const path = require('path');

const JOBS_JSON = path.join(process.env.HOME, '.openclaw', 'cron', 'jobs.json');
const PORT = 3000;
const HOST = '0.0.0.0'; // listen on all interfaces for remote access

function readCronJobs() {
  try {
    const raw = fs.readFileSync(JOBS_JSON, 'utf-8');
    return JSON.parse(raw);
  } catch (e) {
    return { error: e.message };
  }
}

const server = http.createServer((req, res) => {
  if (req.url === '/cron.json') {
    const data = readCronJobs();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
    return;
  }

  if (req.url === '/' || req.url === '/index.html') {
    const html = fs.readFileSync(path.join(__dirname, 'rpg-dashboard.html'), 'utf-8');
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, HOST, () => {
  console.log(`RPG Dashboard listening on http://${HOST}:${PORT}`);
});
