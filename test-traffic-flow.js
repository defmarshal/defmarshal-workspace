const https = require('https');
const API_KEY = 'f6RwVdTvm9EEdWS8X-HhVyIQ-JpXenG1W_XJ0jVo-2Y';

// Test Traffic Flow API endpoint
const url = `https://traffic.ls.hereapi.com/traffic/6.2/flow.json?apiKey=${API_KEY}&bbox=12.0,12.5;13.0,13.5`;

console.log('Testing Traffic Flow API endpoint:', url);
https.get(url, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log(`HTTP ${res.statusCode}`);
    if (data.length > 1000) {
      console.log(data.substring(0, 500) + '...');
    } else {
      console.log(data);
    }
  });
}).on('error', (e) => {
  console.error('Request error:', e.message);
});