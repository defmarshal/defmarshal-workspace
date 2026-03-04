const https = require('https');
const API_KEY = 'f6RwVdTvm9EEdWS8X-HhVyIQ-JpXenG1W_XJ0jVo-2Y';

const origin = '-6.451460,106.735359';
const destination = '-6.241173,106.840765';

const DAYS_BACK = 30;
const TARGET_HOUR = 8;
const CONGESTION_THRESHOLD = 1.3;

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().split('T')[0];
}

function makeUrl(dateStr, hour) {
  let utcHour = hour - 7;
  let departDate = new Date(dateStr + 'T00:00:00');
  if (utcHour < 0) {
    utcHour += 24;
    departDate.setDate(departDate.getDate() - 1);
  }
  const datePart = departDate.toISOString().split('T')[0];
  const depart = `${datePart}T${String(utcHour).padStart(2,'0')}:00:00Z`;
  return `https://router.hereapi.com/v8/routes?transportMode=scooter&origin=${origin}&destination=${destination}&departureTime=${depart}&traffic=enabled&return=polyline,summary,actions&apiKey=${API_KEY}`;
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try { resolve(JSON.parse(data)); }
          catch (e) { reject(new Error('Parse error')); }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0,100)}`));
        }
      });
    }).on('error', reject);
  });
}

(async () => {
  const dailyResults = [];

  console.log(`Predicting traffic for scooter route at ${TARGET_HOUR}:00 (local) — last ${DAYS_BACK} days\n`);

  for (let i = 1; i <= DAYS_BACK; i++) {
    const dateStr = daysAgo(i);
    const url = makeUrl(dateStr, TARGET_HOUR);
    try {
      const json = await fetch(url);
      const section = json.routes[0].sections[0];
      const totalDur = section.summary.duration;
      const totalLength = section.summary.length;
      const baseDur = section.summary.baseDuration || totalDur;
      dailyResults.push({ date: dateStr, totalDuration: totalDur, totalLength: totalLength, baseDuration: baseDur });
      console.log(`${dateStr}: ${Math.round(totalDur/60)} min, base ${Math.round(baseDur/60)}min, ${Math.round(totalLength/1000)} km`);
    } catch (e) {
      console.log(`${dateStr}: ERROR (${e.message})`);
    }
  }

  if (dailyResults.length === 0) {
    console.log('\n❌ No data collected.');
    return;
  }

  const avgTotalDur = dailyResults.reduce((s,d) => s + d.totalDuration, 0) / dailyResults.length;
  const avgBaseDur = dailyResults.reduce((s,d) => s + d.baseDuration, 0) / dailyResults.length;
  const avgLength = dailyResults.reduce((s,d) => s + d.totalLength, 0) / dailyResults.length;
  const minDur = Math.min(...dailyResults.map(d => d.totalDuration));
  const maxDur = Math.max(...dailyResults.map(d => d.totalDuration));

  console.log('\n--- Overall Summary ---');
  console.log(`Samples: ${dailyResults.length}`);
  console.log(`Distance: ~${Math.round(avgLength/1000)} km`);
  console.log(`Avg travel time (with traffic): ${Math.round(avgTotalDur/60)} min`);
  console.log(`Free-flow baseline: ${Math.round(avgBaseDur/60)} min`);
  console.log(`Slowdown factor: ${(avgTotalDur/avgBaseDur).toFixed(2)}×`);
  console.log(`Range: ${Math.round(minDur/60)}–${Math.round(maxDur/60)} min`);

  // Section-level inspection: fetch one recent route and break down sections
  console.log('\n--- Section Congestion Analysis ---');
  try {
    const latest = dailyResults[dailyResults.length - 1];
    const url = makeUrl(latest.date, TARGET_HOUR);
    const json = await fetch(url);
    const route = json.routes[0];
    console.log(`Route contains ${route.sections.length} section(s)`);

    if (route.sections.length > 1) {
      const hotspots = [];
      route.sections.forEach((sec, idx) => {
        const dur = sec.summary.duration;
        const base = sec.summary.baseDuration || dur;
        const ratio = dur / base;
        const isCongested = ratio > CONGESTION_THRESHOLD;
        hotspots.push({ idx, dur, base, ratio, isCongested });
        console.log(`Section ${idx+1}: ${Math.round(dur/60)}min (base ${Math.round(base/60)}min) — ratio ${ratio.toFixed(2)} → ${isCongested ? '🚗 CONGESTED' : '✅ clear'}`);
      });
      // Identify top congested
      hotspots.sort((a,b) => b.ratio - a.ratio);
      if (hotspots[0].isCongested) {
        console.log(`\nTop congestion hotspot: Section ${hotspots[0].idx+1} (ratio ${hotspots[0].ratio.toFixed(2)})`);
      } else {
        console.log('\nNo sections exceed congestion threshold at this hour — traffic is light!');
      }
    } else {
      console.log('HERE returned a single section (coarse-grained). To get segment-level data:');
      console.log('  - Use Traffic Flow API for specific road segments');
      console.log('  - Or split route with intermediate via points to force multi-section response');
    }
  } catch (e) {
    console.log('Section analysis failed:', e.message);
  }

  console.log(`\n✅ Predicted travel time: ${Math.round(avgTotalDur/60)} minutes at ${TARGET_HOUR}:00`);
})();