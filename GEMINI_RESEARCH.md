# Gemini Research Summary: Gradient Traffic Forecasting with HERE

**Date:** 2026-03-04  
**Objective:** Determine resources and approach to forecast traffic along a route with time-dependent congestion (segment arrival times matter).

---

## 1. Core Resources Needed

### A. HERE APIs

| API | Purpose | Key Endpoints |
|-----|---------|---------------|
| **Routing API v8** | Compute routes, get segments, durations, baseDuration | `GET /v8/routes` |
| **Traffic Flow API** | Retrieve historical/real-time speed, jamFactor, freeFlowSpeed for specific road segments (by locationId or corridor) | `GET /traffic/6.2/flow.json` or `/v7/flow` |
| **Geocoding Search API** | Convert place names/addresses to coordinates (and reverse) | `GET /v1/geocode` |
| **Map Attributes API** (optional) | Obtain road metadata (speed limits, road class) | `GET /v1/attributes` |

**Current status:** We already use Routing API v8 successfully. We have not yet integrated Traffic Flow API or Geocoding.

---

## 2. Gradient Forecasting Approaches

### Approach 1: Sequential Segment Queries with Time Adjustment (Using Routing API)

**Concept:**
- Split route into N segments (via waypoints)
- For each segment, compute expected **arrival time** at segment start using cumulative free-flow travel
- Query each segment **independently** at its adjusted departure time
- Sum segment durations for total predicted travel time

**Challenges:**
- The Routing API does not isolate a single segment; you'd need to define tiny origin/destination pairs within the segment, which may return different routes (not the true segment)
- Many API calls (N+1 requests per analysis) → rate limits
- Complex to guarantee the queried sub-route matches the exact segment polyline

**Feasibility:** Low. Better to use Traffic Flow API directly.

---

### Approach 2: Traffic Flow API with Location IDs (Recommended)

**How it works:**
- Traffic Flow API provides `speed`, `freeFlowSpeed`, `jamFactor` for road segments identified by `TMC` location codes or by coordinate-based queries.
- You can query flow for a **corridor** (polyline) and get data for all matching road segments.
- Each flow item includes `SP` (speed), `SU` (free-flow speed), `JF` (jam factor), and timestamps.

**Steps to implement gradient forecast:**
1. Get the full route polyline (from Routing API)
2. Option A: Use the polyline to query flow along a **corridor** (`/flow?corridor=lat,lon;lat,lon;...`)
3. Option B: Map the polyline to TMC location IDs (requires reverse geocoding or map matching)
4. For each flow segment (aligned with the route), we have current/historical speed at time `t`.
5. To simulate progression:
   - Divide route into small distance bins (e.g., 1 km)
   - For each bin, find the corresponding road segment(s)
   - Compute cumulative free-flow time to reach bin start
   - Determine expected arrival time at that bin: `departure + cumulative_free_time`
   - Use flow data for that bin at the expected arrival hour (or interpolate between hourly historical profiles)
   - Compute travel time for that bin: `bin_length / speed_at_time`
6. Sum bin travel times to get total.

**Data requirements:**
- Historical flow data for each road segment for the relevant hour(s) of day and day of week
- HERE provides up to ~90 days of historical flow via the Traffic Flow API (depending on plan)
- You can query flow for a specific timestamp: `starttime=2025-03-03T17:00:00Z&endtime=2025-03-03T18:00:00Z`

**Why this works:** You're not limited to a single departure time query; you dynamically compute expected speeds along the route based on when you would arrive at each point, using historical averages.

---

### Approach 3: Hybrid (Precompute Hourly Profiles)

- For a given route, precompute segment slowdown factors for each hour of day (0–23) by querying traffic once per hour (or using flow data)
- Store in a table: `segment_index × hour → slowdown_ratio`
- Then for any departure time, simulate by stepping through segments and looking up the appropriate hour based on cumulative free-flow cumulative time
- Reduces real-time queries; just table lookups

---

## 3. Geocoding for Landmark Input

- **Geocoding Search API** (`/v1/geocode`): `q={query}&apiKey=...`
  - Accepts free-form addresses, place names, landmarks
  - Returns bounding box and position (lat, lon)
  - Autocomplete available via `/v1/autosuggest` or `/v1/geocode` with `types=place`
- **Integration:** Add a text input; on submit, call geocode; fill origin/dest fields with results.
- Example: `q=Grand+Indonesia+Jakarta` returns coordinates.

---

## 4. Practical Implementation Plan

### Phase 1: Geocoding Integration
- Add two text inputs for "Origin place" and "Destination place" alongside numeric lat/lon
- On blur or button click, call HERE Geocoding API
- Populate lat/lon fields and map

### Phase 2: Traffic Flow API Exploration
- Test a simple flow query along the route corridor
- Understand response structure: `FIS` → `FI` → `TMC`, `SP`, `SU`, `JF`
- Determine how to match flow items to specific points along the route (spatial join)

### Phase 3: Hourly Profile Generation (Batch)
- For a given route (segmented), query flow for each hour of a representative weekday (e.g., 00:00–23:00)
- Build a lookup table: `[segmentIndex][hour] → speed, slowdown`
- Cache this table (localStorage or server)

### Phase 4: Gradient Simulation
- User selects departure time
- For each segment i:
  - `arrivalHour = floor( (departureTime + cumulativeFreeTime_i) % 24 )`
  - Lookup `speed = profile[i][arrivalHour]`
  - Compute segment duration = `segmentLength / speed`
- Sum durations → total forecasted travel time
- Optionally visualize a speed profile along the route

---

## 5. Constraints & Quotas

- **Rate limits:** Vary by plan; free tier typically has requests per day and per minute limits
- **Historical window:** Traffic Flow API usually provides last 90 days of data
- **Segments:** MORE SEGMENTS = more flow items to process; but also more precise
- **Caching:** Essential to avoid re-querying the same flow data repeatedly

---

## 6. Conclusion

**Recommended path:** Implement **Approach 2** using Traffic Flow API to get actual speed profiles per road segment, then simulate arrival times along the route. This gives true gradient forecasting.

We must also add **Geocoding** to accept place names, as requested.

Our current hotspot analyzer (Routing API with via points) is a good approximation for a **single departure time**, but it does not account for time progression. To achieve gradient forecasting, we need to move to flow-based speed lookup per segment per hour.

---

*End of Gemini research summary.*