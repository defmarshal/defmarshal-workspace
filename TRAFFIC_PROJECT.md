# Traffic Forecasting with Historical Data — Project Log

**Date:** 2026-03-04  
**Goal:** Forecast traffic along a route based on historical patterns, accounting for **time‑varying congestion** throughout the trip (not just at departure).

---

## 🎯 End Goal

When traveling from A to B, traffic conditions change as the day progresses. For example, if you depart at 5 PM, the first 10 km might be congested, but the next 10 km could be clear — and by the time you reach the midway point, the effective "departure time" for that segment is later than your start time.

**Desired behavior:**
- Slice the route into segments
- For each segment, compute its expected arrival time based on cumulative travel up to that point
- Look up historical traffic for that segment at the **expected arrival time** (not just the global departure time)
- Aggregate segment predictions to get a total travel time that reflects **gradient traffic evolution**

This is more accurate than a single `duration` query with a static `departureTime`.

---

## 📊 Progress So Far

### 1. Basic Route Visualization & Multi‑Time Comparison
- Built `route-viz.html` showing route on map
- Fetches travel time for multiple departure times (05:00, 05:30, 06:00, 17:00)
- Compares `duration` vs `baseDuration` to compute slowdown
- Discovered: `baseDuration` is the free‑flow baseline included in the same response (`traffic=enabled`)
- Using **car** transport yields realistic congestion; **scooter** shows near‑free‑flow even during rush hour

### 2. Hotspot Analyzer with Waypoint Splitting
- Built `route-hotspots.html`
- Splits route into segments by sampling waypoints from the full route polyline
- Uses multiple `&via=` parameters to force HERE Routing API to return **multiple sections**
- Computes slowdown per segment: `duration / baseDuration`
- Visualizes segments with color‑coding (green/orange/red)
- Shows table with segment‑level metrics

### 3. Alternative Routes
- Added support for fetching **multiple alternative paths** (`alternatives=N`)
- All routes drawn on map simultaneously with distinct colors
- Legend with checkboxes to show/hide each route
- Dropdown to select which route to analyze hotspots for
- **Swap button** to instantly reverse origin/destination

---

## ⚠️ Current Limitations

1. **Single departure time per analysis**  
   The hotspot analysis still uses a fixed `departureTime` for all segments. It does **not** account for the fact that you reach each segment at a different clock time.

2. **Waypoint sampling may not align with road network nodes**  
   Our method samples points from the polyline; these points happen to be on drivable roads (so far successful). But the number of segments is limited by how many waypoints we feed.

3. **No gradient time adjustment**  
   To forecast accurately, we need to:
   - Compute cumulative travel time from start to the beginning of each segment (using free‑flow speeds)
   - Add that to departure time to get segment‑specific departure time
   - Query traffic for that segment at that computed time (or use Traffic Flow API with time dimension)

4. **Coordinate input**  
   Users must enter raw `lat,lon`. We'd like to support **place names / landmarks** (e.g., "Grand Indonesia", "Soekarno‑Hatta Airport") like Google Maps.

5. **API rate limits & historical window**  
   HERE historical traffic typically covers last 90 days. Our tests used `2026-01-15` (a past date) to get realistic congestion.

---

## 🔬 Research Questions

### Q1: Can we input coordinates based on landmarks?
- HERE has a **Geocoding API** (`/v1/geocode`) that converts addresses/place names to coordinates.
- Example: `https://geocode.search.hereapi.com/v1/geocode?q=Grand%20Indonesia&apiKey=YOUR_KEY`
- We could integrate this to let users type familiar names instead of raw lat/lon.

### Q2: How to implement gradient traffic forecasting?
Two possible approaches:

**Approach A: Sequential segment queries with adjusted departure times**
1. Get full route polyline (no waypoints) → summary gives total `baseDuration` (free‑flow)
2. Divide route into N segments by distance (e.g., 5 segments)
3. For each segment i:
   - Compute cumulative free‑flow time from start to segment i: `t_i`
   - Segment departure time = `global_departure + t_i`
   - Query a **short route** that isolates that segment only? Not trivial.
   - Alternatively, use Traffic Flow API to get speed at a specific coordinate and time.

**Approach B: Use HERE Traffic Flow API directly**
- Traffic Flow API provides `speed`, `freeFlowSpeed`, `jamFactor` for road segments by `locationId` and time.
- We could:
  1. Map the route to TMC location IDs (requires reverse‑geocoding or `map-matching`).
  2. For each location ID, query flow data at the time we expect to be there.
  3. Compute travel time per segment using current speed vs free‑flow speed.
- This is more precise but requires additional API permissions and a different data model.

**Approach C: Hybrid**
- Use the multi‑section route we already have (via waypoints) as segments.
- For each section, we have `baseDuration` (free‑flow) and `duration` (with traffic) **at the global departure time**.
- To adjust for time progression, we could:
  - Assume traffic on a segment scales with the time of day curve derived from historical data at that location.
  - Fetch historical traffic for the same route at multiple times (e.g., every hour) and interpolate segment slowdown as a function of time.
  - Then, for a given departure, simulate the trip by stepping through segments and adjusting slowdown based on the current simulated clock.

This is more complex but doable with multiple queries.

---

## 🛠️ Technical Notes

- **HERE API endpoint:** `https://router.hereapi.com/v8/routes`
- Parameters:
  - `transportMode`: car, scooter, bicycle, pedestrian
  - `origin`, `destination`: lat,lon
  - `departureTime`: ISO 8601 UTC (convert from local)
  - `traffic=enabled` includes traffic (response has `summary.duration` and `summary.baseDuration`)
  - `alternatives=N` returns multiple routes
  - `via=lat,lon` (repeated) forces segmentation
- **Polyline format:** HERE Flex Polyline (decoder implemented in JS)
- **Timezone:** Local is UTC+7 (WIB); convert to UTC by subtracting 7 hours (handle day wrap)

---

## 📝 Next Steps

1. **Integrate Geocoding** to allow place name input
2. **Implement gradient time forecasting**:
   - Choose a segmentation strategy (e.g., 5–10 equal‑length segments)
   - For each segment, estimate arrival time using free‑flow speeds
   - Query Traffic Flow API or use a pre‑computed hourly traffic profile to adjust segment duration
3. **Visualization:** Show a timeline chart of speed/slowdown along the route
4. **Persist settings:** Remember last used coordinates, date, transport mode
5. **Export data:** Allow CSV export of segment‑level predictions

---

## 🧠 Lessons Learned

- The HERE Routing API's `baseDuration` is a clean free‑flow baseline (no need for separate `traffic=disabled` which is invalid)
- Multi‑section routing requires `&via=` repeated parameters (not semicolon‑joined)
- Waypoints must be on valid roads; sampling from an existing route polyline ensures this
- Different transport modes show very different congestion patterns (cars > scooters)
- Historical date matters; using a date within the last 90 days yields realistic traffic

---

*End of log.*