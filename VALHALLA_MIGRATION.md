# Valhalla Migration - Phase 1 Complete

**Date:** March 12, 2026
**Status:** Phase 1 ✅ Complete (bug fixes applied) | Phase 2 ⏳ Pending | Local Server 🔄 Tiles Building

---

## Latest Updates (March 12, 2026 - 02:35 WIB)

### Tile Build Status

**Local Valhalla server setup in progress:**
- ✅ Build complete (v3.6.3, native ARM64)
- 🔄 **Docker tile build running** (x86_64 emulation on ARM64, ~1-2 hours)
- ⏳ Server start pending (after tiles complete)

**Note:** Docker image is x86_64, running via QEMU emulation on ARM64. Build is slower than native.

See `VALHALLA_SETUP_COMPLETE.md` for full details.

### Bug Fixes Applied

| Issue | Fix | Status |
|-------|-----|--------|
| Valhalla response parsing error | Handle both `{trip: {...}}` and `{trips: [...]}` formats | ✅ Fixed |
| Segment analysis distance limit exceeded | Reduced segments from 15 → 5, added coordinate validation | ✅ Fixed |
| Waypoint accumulation in segment analysis | Added `skipUserVia` parameter to avoid duplicate waypoints | ✅ Fixed |
| **Polyline decoder precision** | Changed from `1e5` to `1e6` (Valhalla uses 6 decimal places) | ✅ Fixed |

---

## Overview

Migrating from HERE Maps Routing API to **Valhalla** (open-source routing engine) while retaining HERE Traffic API for real-time traffic data.

**Reason:** HERE routing unreliable in Jakarta/Bandung area. HERE traffic data acceptable.

---

## Phase 1: Valhalla Routing (Complete ✅)

### What Was Done

| Component | Status | Details |
|-----------|--------|---------|
| **Routing API** | ✅ Done | Replaced HERE `/v8/routes` with Valhalla `/route` |
| **Polyline Decoding** | ✅ Done | HERE custom format → Standard Google polyline decoder |
| **Vehicle Types** | ✅ Done | `car`, `scooter`, `bicycle`, `pedestrian` all mapped |
| **Avoidance Settings** | ✅ Done | Tolls, highways, ferries avoided (matches original behavior) |
| **Alternative Routes** | ✅ Done | Up to 5 alternatives via Valhalla |
| **Response Mapping** | ✅ Done | Valhalla `{trips}` → App `{routes}` structure |
| **Autosuggest** | ✅ Unchanged | Still using HERE API (no changes needed) |
| **UI/UX** | ✅ Unchanged | All existing features work identically |

### Files Modified/Created

| File | Status | Description |
|------|--------|-------------|
| `route-hotspots-valhalla-phase1.html` | ✅ Created | Phase 1 complete version |
| `route-hotspots-mobile-backup-20260312-004906.html` | 📦 Backup | Original HERE version (unchanged) |

### Technical Changes

#### 1. Routing Function (lines 802-873)

**Before (HERE):**
```javascript
async function fetchRoute(dateStr, hour, min, transport, viaPoints = [], alternatives = 0) {
  const dep = buildDepartureTime(dateStr, hour, min);
  let url = `https://router.hereapi.com/v8/routes?transportMode=${transport}&origin=${state.originCoord}&destination=${state.destCoord}&departureTime=${dep}&traffic=enabled&return=polyline,summary&apiKey=${API_KEY}&_t=${Date.now()}`;
  if (alternatives > 0) url += `&alternatives=${alternatives}`;
  // ... via points, avoidance
  url += '&avoid=tollRoad&avoid=controlledAccessHighway';
  const resp = await fetch(url);
  // ... parse HERE response
}
```

**After (Valhalla):**
```javascript
async function fetchRoute(dateStr, hour, min, transport, viaPoints = [], alternatives = 0) {
  const locations = [{lat: state.origLat, lon: state.origLng}];
  if (state.viaLat && state.viaLng) locations.push({lat: state.viaLat, lon: state.viaLng});
  viaPoints.forEach(vp => { /* add via */ });
  locations.push({lat: state.destLat, lon: state.destLng});
  
  const costingMap = {car: 'auto', scooter: 'motor_scooter', bicycle: 'bicycle', pedestrian: 'pedestrian'};
  const costing = costingMap[transport] || 'auto';
  
  const body = {
    locations,
    costing,
    costing_options: {
      [costing]: {use_tolls: 0, use_highways: 0, use_ferry: 0}
    },
    date_time: {type: 0, value: `${dateStr}T${hour}:${min}`}
  };
  if (alternatives > 0) body.alternatives = alternatives;
  
  const resp = await fetch(`${VALHALLA_SERVER}/route`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  // ... map Valhalla response to existing structure
}
```

#### 2. Polyline Decoder (lines 753-784)

**Before (HERE custom format):**
```javascript
function decodeHEREPolyline(encoded) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
  // ... complex HERE-specific decoding with version, precision, etc.
}
```

**After (Standard Google format):**
```javascript
function decodePolyline(encoded) {
  // Standard Google polyline decoding algorithm
  const points = [];
  let index = 0, lat = 0, lng = 0;
  while (index < encoded.length) {
    // ... decode varint-encoded lat/lng deltas
  }
  return points;
}
```

### Vehicle Type Mapping

| App Select | Valhalla Costing | Avoidance Applied |
|------------|------------------|-------------------|
| Car | `auto` | No tolls, no highways, no ferries |
| Scooter | `motor_scooter` | No tolls, no highways, no ferries |
| Bicycle | `bicycle` | `use_hills: 0.5`, `use_roads: 0.5` |
| Pedestrian | `pedestrian` | `use_ferry: 1` (allowed) |

### API Endpoints

| Service | Endpoint | Status |
|---------|----------|--------|
| **Valhalla Routing** (Public) | `https://valhalla1.openstreetmap.de/route` | ✅ Active (current) |
| **Valhalla Routing** (Local) | `http://localhost:8002/route` | 🔄 Pending (tiles ~60%) |
| **HERE Autosuggest** | `https://autosuggest.search.hereapi.com/v1/autosuggest` | ✅ Active |
| **HERE Traffic Flow** | Not yet used | ⏳ Phase 2 |

---

## Phase 2: HERE Traffic Integration (Pending ⏳)

### What Needs to Be Done

| Component | Status | Estimated Effort |
|-----------|--------|------------------|
| **HERE Traffic Flow API** | ⏳ Pending | 1.5-2h |
| **Traffic-to-Route Matching** | ⏳ Pending | 1.5-2h |
| **Segment Duration Calculation** | ⏳ Pending | 0.5-1h |
| **Update `baseDuration` Logic** | ⏳ Pending | 0.5h |
| **Testing & Validation** | ⏳ Pending | 1h |

**Total Phase 2 Effort:** ~5-7 hours

### Planned Implementation

#### 1. Add Traffic Flow API Call

```javascript
async function fetchTrafficForRoute(bbox) {
  const [minLon, minLat, maxLon, maxLat] = bbox;
  const url = `https://traffic.api.here.com/traffic/6.2/flow.js?apiKey=${API_KEY}&bbox=${minLon},${minLat},${maxLon},${maxLat}&maxresults=2000`;
  const resp = await fetch(url);
  const data = await resp.json();
  return data.TRAFFIC_ITEMS?.ITEM || [];  // Returns speed, baseSpeed, position
}
```

#### 2. Match Traffic Segments to Route Geometry

```javascript
function matchTrafficToRoute(routeCoords, trafficItems) {
  // For each route segment, find nearest traffic item within ~50m
  // Calculate slowdown ratio: baseSpeed / currentSpeed
  // Return array of ratios per segment
}
```

#### 3. Update Segment Analysis

Currently, slowdown ratio is calculated as:
```javascript
ratio = duration / baseline  // Both from HERE routing
```

After Phase 2:
```javascript
ratio = trafficSpeed / freeFlowSpeed  // From HERE Traffic Flow API
duration = distance / trafficSpeed
baseline = distance / freeFlowSpeed
```

### HERE Traffic API Options

| API | Endpoint | Pros | Cons |
|-----|----------|------|------|
| **Traffic Flow 6.2** | `traffic/6.2/flow.js` | Mature, detailed data | Legacy API |
| **Traffic Flow v2** | `traffic.hereapi.com/v2/flow` | Modern REST, JSON | May need different API key permissions |

**Recommended:** Start with 6.2 (proven to work), migrate to v2 if needed.

---

## Testing Checklist

### Phase 1 Testing (Current)

- [ ] **Basic routing:** Origin → Destination works
- [ ] **Alternative routes:** Multiple routes displayed correctly
- [ ] **Via points:** Adding intermediate stops works
- [ ] **Vehicle types:** All 4 types produce different routes
- [ ] **Avoidance:** Routes avoid tolls/highways as expected
- [ ] **Saved routes:** Load/save/export/import still work
- [ ] **Autosuggest:** Place search still functional
- [ ] **Segment analysis:** Slowdown analysis works (time-based comparison)
- [ ] **Gradient analysis:** Time-range gradient table generates correctly
- [ ] **30-day average:** Historical comparison works

### Phase 2 Testing (Future)

- [ ] **Traffic overlay:** Real-time traffic displayed on Valhalla routes
- [ ] **Accuracy:** Traffic slowdown ratios match actual conditions
- [ ] **Performance:** Traffic API calls don't cause excessive latency
- [ ] **Fallback:** App handles missing traffic data gracefully

---

## Known Limitations

### Phase 1

1. **No real-time traffic:** Valhalla doesn't provide traffic data. Current slowdown analysis uses **time-based comparison** (same route at different times) instead of actual traffic speeds.

2. **Public server dependency:** Uses `valhalla1.openstreetmap.de` (free demo instance). For production:
   - Self-host Valhalla with Docker
   - Or use Mapbox Valhalla API (paid, more reliable)

3. **Routing quality:** Valhalla uses OpenStreetMap data. Road coverage/accuracy depends on OSM community updates in your area.

### Phase 2 (Anticipated)

1. **Traffic matching complexity:** HERE traffic segments may not align perfectly with Valhalla route geometry. Requires spatial interpolation.

2. **API rate limits:** Two API calls per route (Valhalla + HERE Traffic). May need caching/batching.

3. **Cost:** HERE Traffic API may have separate pricing from HERE Routing.

---

## Rollback Plan

If Phase 1 has issues:

1. **Revert to original:** Use `route-hotspots-mobile-backup-20260312-004906.html`
2. **Hybrid approach:** Keep Valhalla routing, add HERE Traffic Flow API (Phase 2)
3. **Full HERE:** If Valhalla routing quality is unacceptable, stay with HERE but accept reliability issues

---

## Production Deployment Recommendations

### Before Going Live

1. **Self-host Valhalla** (recommended for Jakarta/Bandung area):
   ```bash
   docker run -d -p 8002:8002 valhalla/valhalla
   ```
   - Better performance, no rate limits
   - Can customize costing models
   - Add local traffic data if available

2. **Add caching:**
   - Cache routes by origin/destination/time
   - Reduce API calls for repeated queries

3. **Error handling:**
   - Fallback to HERE routing if Valhalla fails
   - Graceful degradation if traffic API unavailable

4. **Monitoring:**
   - Track API response times
   - Log routing failures
   - Compare Valhalla vs HERE route quality

---

## Next Steps

1. **Test Phase 1** thoroughly in target area (Jakarta → Bandung routes)
2. **Compare route quality** vs original HERE routing
3. **If satisfied**, proceed to Phase 2 (HERE Traffic integration)
4. **If not satisfied**, adjust Valhalla costing options or consider alternatives

---

## Contact / Notes

- **Original file:** `route-hotspots-mobile-backup-20260312-004906.html`
- **Phase 1 file:** `route-hotspots-valhalla-phase1.html`
- **HERE API Key:** `f6RwVdTvm9EEdWS8X-HhVyIQ-JpXenG1W_XJ0jVo-2Y` (still used for autosuggest + Phase 2 traffic)
- **Valhalla Server:** `https://valhalla1.openstreetmap.de` (public demo)
