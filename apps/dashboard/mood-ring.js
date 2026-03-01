// 🔑 mewmew Mood Ring — live display in ClawDash

let moodRingLoaded = false;
let moodRingInterval = null;

function getMoodRing() {
  fetch('/api/mood-ring')
    .then(r => r.json())
    .then(data => {
      if (!data.ok) return;
      
      const moodEl = document.getElementById('mood-ring-status');
      if (!moodEl) return;
      
      moodEl.innerHTML = `
        <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;background:var(--surface);border-radius:8px">
          <span style="font-size:14px;font-weight:600;color:var(--text)">${data.mood.emoji} ${data.mood.text}</span>
          <span style="font-size:11px;color:var(--muted);flex:1;text-align:right">${data.mood.timestamp}</span>
        </div>
        <div style="font-size:10px;color:var(--muted);margin-top:4px">${data.mood.reflection}</div>
      `;
      
      // Update connection dot color
      const dot = document.getElementById('connection-dot');
      if (dot) {
        dot.style.backgroundColor = data.mood.emoji.includes('🚀') ? '#4CAF50' :
                                  data.mood.emoji.includes('🤖') ? '#2196F3' :
                                  data.mood.emoji.includes('🧠') ? '#FF9800' :
                                  '#9C27B0';
      }
    })
    .catch(err => {
      console.log('Mood Ring error:', err);
    });
}

function startMoodRing() {
  if (moodRingLoaded) return;
  moodRingLoaded = true;
  
  // Add mood ring panel to Overview tab
  const overview = document.getElementById('tab-overview');
  if (overview) {
    const moodPanel = document.createElement('div');
    moodPanel.id = 'mood-ring-panel';
    moodPanel.className = 'card';
    moodPanel.innerHTML = `
      <h2 style="display:flex;align-items:center;gap:8px">
        <span>🔑 mewmew Mood Ring</span>
        <span id="connection-dot" style="width:8px;height:8px;border-radius:50%;background:#9C27B0;flex-shrink:0"></span>
      </h2>
      <div id="mood-ring-status" style="min-height:60px;padding:8px;background:var(--surface2);border-radius:6px">
        <div style="text-align:center;padding:15px;color:var(--muted)">Loading mood...</div>
      </div>
    `;
    overview.appendChild(moodPanel);
  }
  
  // Update every 5 minutes
  moodRingInterval = setInterval(getMoodRing, 5 * 60 * 1000);
  getMoodRing(); // initial load
}

// Start when dashboard loads
document.addEventListener('DOMContentLoaded', startMoodRing);
