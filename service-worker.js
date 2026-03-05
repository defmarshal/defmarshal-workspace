const CACHE = 'hotspot-v1';
const ASSETS = [
  './',
  'route-hotspots.html',
  'manifest.json',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  // Only handle same-origin or whitelisted assets
  const url = e.request.url;
  const isOurAsset = ASSETS.includes(url) || url.startsWith(self.location.origin);
  if (isOurAsset) {
    e.respondWith(
      caches.match(e.request).then(r => r || fetch(e.request))
    );
  }
});
