# Valhalla Routing Engine - Complete Setup Guide

**Status:** ✅ Build Complete | 🔄 Docker Tile Build Running | ⏳ Server Pending
**Last Updated:** 2026-03-12 02:35 WIB
**Platform:** Ubuntu 24.04 ARM64 (Native Build)

---

## 📊 Current Setup Progress

| Step | Status | Details |
|------|--------|---------|
| **1. Dependencies** | ✅ Complete | All build deps installed (Boost, Protobuf, LuaJIT, etc.) |
| **2. Source Code** | ✅ Complete | Valhalla 3.6.3 cloned from GitHub |
| **3. Build** | ✅ Complete | Native ARM64 build (~45 min) |
| **4. Installation** | ✅ Complete | Binaries in `/usr/local/bin` |
| **5. Tile Build** | 🔄 Running | Docker x86_64 emulation on ARM64 (~1-2 hours) |
| **6. Server Start** | ⏳ Pending | Will start after tiles complete |
| **7. Testing** | ⏳ Pending | Route API test pending |

---

## 🔄 Current Build Status (02:35 WIB)

**Docker tile build in progress:**
- Running via QEMU x86_64 emulation on ARM64
- Expected duration: 1-2 hours (slower than native due to emulation)
- Build log: `memory/valhalla-docker-build.log`

**To check progress:**
```bash
# Check if build is still running
ps aux | grep valhalla_build_tiles

# Check tiles directory size
du -sh /home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/tiles/tiles/

# View build log
tail -f /home/ubuntu/.openclaw/workspace/memory/valhalla-docker-build.log
```

---

## 🏗️ Build Summary (ARM64 Native)

### What Was Installed

**Build Dependencies:**
```bash
cmake, g++, make, pkg-config
libboost-all-dev (1.83)
libprotobuf-dev, protobuf-compiler (3.21.12)
libsqlite3-dev, libspatialite-dev
libcurl4-openssl-dev, libssl-dev
libgeos-dev, libproj-dev
liblua5.3-dev, luajit (2.1.0)
libbz2-dev, liblz4-dev, libzstd-dev
libtbb-dev, libxml2-dev, libzip-dev
```

**Build Configuration:**
```bash
cmake -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_PYTHON_BINDINGS=OFF \
  -DENABLE_NODEJS_BINDINGS=OFF \
  -DENABLE_SERVICES=OFF \
  -DENABLE_TOOLS=ON \
  -DBUILD_TESTING=OFF \
  -DENABLE_TESTS=OFF
```

**Installed Binaries:**
- `/usr/local/bin/valhalla_service` - HTTP service (needs prime_server)
- `/usr/local/bin/valhalla_build_tiles` - Tile builder
- `/usr/local/bin/valhalla_build_extract` - Tile indexer
- `/usr/local/bin/valhalla_build_admins` - Admin boundary builder
- `/usr/local/bin/valhalla_build_timezones` - Timezone builder
- `/usr/local/bin/valhalla_add_elevation` - Elevation data tool
- `/usr/local/bin/valhalla_add_landmarks` - Landmark tool
- `/usr/local/bin/valhalla_assign_speeds` - Speed assignment tool

**Version:** Valhalla 3.6.3 (latest stable)

---

## 📚 Official Documentation Reference

### Documentation Links

| Resource | URL |
|----------|-----|
| Main Documentation | https://valhalla.github.io/valhalla |
| Building Instructions | https://valhalla.github.io/valhalla/building/ |
| Turn-by-Turn API | https://valhalla.github.io/valhalla/api/turn-by-turn/ |
| Isochrone API | https://valhalla.github.io/valhalla/api/isochrone/ |
| Matrix API | https://valhalla.github.io/valhalla/api/matrix/ |
| Demo Server | https://valhalla.app |
| Demo API | https://api.valhalla.app |

### Module Architecture

| Module | Purpose |
|--------|---------|
| **Midgard** | Geographic/geometric algorithms |
| **Baldr** | Base data structures for tiled route data |
| **Sif** | Graph node/edge costing library |
| **Skadi** | Elevation data service |
| **Mjolnir** | OSM → Valhalla graph tile conversion |
| **Loki** | Graph search & location correlation |
| **Meili** | Map-matching library |
| **Thor** | Path generation through graph tiles |
| **Odin** | Maneuver & narrative generation |
| **Tyr** | HTTP request handler & JSON output |

---

## 🌐 API Reference

### Available Endpoints (localhost:8002)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/route` | POST/GET | Turn-by-turn routing |
| `/isochrone` | POST/GET | Reachable areas (time/distance) |
| `/sources_to_targets` | POST/GET | Time-distance matrix |
| `/locate` | POST/GET | Map matching / correlation |
| `/optimize` | POST/GET | Tour optimization (TSP) |
| `/status` | GET | Server status |
| `/height` | POST/GET | Elevation lookup |

---

### 1. Route API (Turn-by-Turn)

**Endpoint:** `POST localhost:8002/route?json={REQUEST}`

**Basic Request:**
```json
{
  "locations": [
    {"lat": -6.2088, "lon": 106.8456, "city": "Jakarta"},
    {"lat": -6.9175, "lon": 107.6191, "city": "Bandung"}
  ],
  "costing": "auto",
  "units": "kilometers"
}
```

**Costing Models:**
| Model | Description |
|-------|-------------|
| `auto` | Car, motorcycle, truck (default) |
| `bicycle` | Bicycle with cycleway preference |
| `bus` | Bus routes |
| `truck` | Truck with dimensional restrictions |
| `taxi` | Taxi with lane access |
| `motor_scooter` | Moped/scooter (BETA) |
| `motorcycle` | Motorcycle touring (BETA) |
| `pedestrian` | Walking routes |
| `multimodal` | Pedestrian + transit (BETA) |

**Auto Costing Options:**
```json
{
  "costing": "auto",
  "costing_options": {
    "auto": {
      "use_tolls": 0,           // Avoid tolls (0-1)
      "use_highways": 0,        // Avoid highways (0-1)
      "use_ferry": 0,           // Avoid ferries (0-1)
      "shortest": false,        // Distance-only costing
      "maneuver_penalty": 5,    // Seconds penalty for turns
      "gate_cost": 30,          // Cost for private gates
      "toll_booth_cost": 15     // Cost at toll booths
    }
  }
}
```

**Bicycle Costing Options:**
```json
{
  "costing": "bicycle",
  "costing_options": {
    "bicycle": {
      "bicycle_type": "hybrid",  // road, hybrid, cross, mountain
      "cycling_speed": 20,       // km/h
      "use_roads": 0.5,          // Road tolerance (0-1)
      "use_hills": 0.5,          // Hill tolerance (0-1)
      "avoid_bad_surfaces": 0.25 // Surface avoidance (0-1)
    }
  }
}
```

**Pedestrian Costing Options:**
```json
{
  "costing": "pedestrian",
  "costing_options": {
    "pedestrian": {
      "walking_speed": 5.1,      // km/h
      "use_hills": 0.5,
      "step_penalty": 30,        // Seconds per step
      "max_hiking_difficulty": 1 // SAC scale 0-6
    }
  }
}
```

**Response Format:**
```json
{
  "trip": {
    "status": 0,
    "status_message": "Found route between points",
    "units": "kilometers",
    "language": "en-US",
    "summary": {
      "time": 7200,        // seconds
      "length": 150.5,     // km
      "has_toll": false,
      "has_highway": true,
      "min_lat": -6.9175,
      "min_lon": 106.8456,
      "max_lat": -6.2088,
      "max_lon": 107.6191
    },
    "locations": [...],
    "legs": [
      {
        "summary": {...},
        "shape": "encoded_polyline_6_digit_precision",
        "maneuvers": [
          {
            "type": 1,
            "instruction": "Drive east on Jalan Sudirman.",
            "time": 120,
            "length": 2.5,
            "begin_shape_index": 0,
            "end_shape_index": 15
          }
        ]
      }
    ]
  }
}
```

---

### 2. Isochrone API

**Endpoint:** `POST localhost:8002/isochrone?json={REQUEST}`

**Request:**
```json
{
  "locations": [{"lat": -6.2088, "lon": 106.8456}],
  "costing": "auto",
  "contours": [
    {"time": 15, "color": "ff0000"},
    {"time": 30, "color": "00ff00"},
    {"time": 45, "color": "0000ff"}
  ],
  "polygons": true,
  "denoise": 0.5,
  "generalize": 50
}
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| `locations` | Center point (lat/lon) |
| `costing` | Route costing model |
| `contours` | Array of time (min) or distance (km) intervals |
| `polygons` | Return polygons (true) or linestrings (false) |
| `denoise` | Remove small contours (0-1, default 1) |
| `generalize` | Douglas-Peucker tolerance in meters |
| `reverse` | Inverse expansion (reachability TO location) |

**Response:** GeoJSON FeatureCollection

---

### 3. Matrix API

**Endpoint:** `POST localhost:8002/sources_to_targets?json={REQUEST}`

**Request:**
```json
{
  "sources": [
    {"lat": -6.2088, "lon": 106.8456},
    {"lat": -6.1751, "lon": 106.8650}
  ],
  "targets": [
    {"lat": -6.9175, "lon": 107.6191},
    {"lat": -7.7956, "lon": 110.3695}
  ],
  "costing": "auto",
  "verbose": true
}
```

**Response (verbose=true):**
```json
{
  "sources": [...],
  "targets": [...],
  "sources_to_targets": [
    {
      "distance": 150.5,
      "time": 7200,
      "from_index": 0,
      "to_index": 0
    },
    ...
  ]
}
```

**Response (verbose=false):**
```json
{
  "sources_to_targets": {
    "durations": [[7200, 14400], [6800, 13900]],
    "distances": [[150.5, 290.2], [142.3, 280.1]]
  }
}
```

---

## 🔧 Configuration Files

### valhalla.json (Server Config)

```json
{
  "mjolnir": {
    "tile_dir": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/tiles",
    "tile_extract": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/tiles.tar",
    "admin_filename": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/tiles/admins.bin",
    "time_zone_filename": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/tiles/time_zones.bin",
    "use_elevation": false
  },
  "locality": {
    "locale_file": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/config/locality.json"
  },
  "http_service": {
    "listening_port": 8002,
    "address": "0.0.0.0"
  },
  "logging": {
    "type": "info",
    "file_name": "/home/ubuntu/.openclaw/workspace/valhalla-jabodetabek/data/valhalla.log"
  }
}
```

### locality.json (Indonesia Config)

```json
{
  "localities": [
    {
      "name": "ID",
      "drive_on_right": false,
      "internal": false
    }
  ]
}
```

---

## 📦 Data Sources

### OSM Data Sources

| Source | URL | Coverage |
|--------|-----|----------|
| **Geofabrik** | https://download.geofabrik.de/ | Global (country/region extracts) |
| **BBBike** | https://download.bbbike.org/osm/ | Metro areas |
| **OpenStreetMap** | https://planet.osm.org/ | Full planet |

**Current Data:** Indonesia extract (1.6GB) from Geofabrik
- Covers: Jakarta, Bogor, Depok, Tangerang, Bekasi (Jabodetabek)
- Bounding box: `106.529,-6.714,107.097,-6.014`

### Additional Data (Optional)

| Data Type | Source | Purpose |
|-----------|--------|---------|
| **Elevation** | AWS Terrain Tiles / SRTM | Elevation-based routing |
| **Transit** | GTFS feeds | Public transport routing |
| **Traffic** | HERE Traffic API / TomTom | Real-time traffic |

---

## 🚀 Quick Start Commands

### Build Tiles (One-Time Setup)

**Current Build Status (2026-03-12 01:58 WIB):**
- Process: `valhalla_build_tiles` (PID 2512252)
- Started: 01:49 WIB (~10 minutes ago)
- Progress: ~60% complete
- Tiles generated: ~6 GB
- ETA: ~30-45 minutes remaining

**Tile Files Generated:**
| File | Size | Status |
|------|------|--------|
| `way_nodes.bin` | 2.9 GB | ✅ |
| `ways.bin` | 1.7 GB | ✅ |
| `nodes.bin` | 1.0 GB | ✅ |
| `edges.bin` | 336 MB | 🔄 Writing |
| `access.bin` | 83 MB | ✅ |
| `complex_*_restrictions.bin` | ~1.3 MB | ✅ |
| `linguistics_node.bin` | 4 KB | ✅ |

```bash
cd /home/ubuntu/.openclaw/workspace/valhalla-jabodetabek
valhalla_build_tiles -c config/valhalla_build.json data/jabodetabek.osm.pbf
```

### Create Tile Extract (Optional, for faster loading)
```bash
valhalla_build_extract -c config/valhalla_build.json -v
```

### Start Server
```bash
valhalla_service config/valhalla.json 1
```

### Test Route
```bash
curl "http://localhost:8002/route?json={
  \"locations\":[
    {\"lat\":-6.2088,\"lon\":106.8456},
    {\"lat\":-6.9175,\"lon\":107.6191}
  ],
  \"costing\":\"auto\",
  \"units\":\"kilometers\"
}" | jq '.'
```

### Check Status
```bash
curl http://localhost:8002/status
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Port 8002 in use** | `lsof -i :8002` then `kill <PID>` |
| **Tiles not found** | Run `valhalla_build_tiles` first |
| **Route not found** | Check OSM data coverage, increase search radius |
| **Slow routing** | Enable tile extract, increase RAM |
| **Memory errors** | Reduce tile coverage, add swap space |

### Log Files

| Log | Location |
|-----|----------|
| **Build Log** | `memory/valhalla-build.log` |
| **Tile Build** | `memory/valhalla-tile-build.log` |
| **Server Log** | `data/valhalla.log` |

---

## 📈 Performance Tips

1. **Use SSD Storage** - Tile loading is I/O intensive
2. **Enable Tile Extract** - Faster graph loading with `.tar` file
3. **Allocate RAM** - 4-8 GB recommended for caching
4. **Enable Elevation** - More accurate routing (adds ~1 GB)
5. **Tune Alternatives** - Balance quality vs. speed

---

## 🔗 Integration with Existing App

### Update `route-hotspots-valhalla-phase1.html`

Change the Valhalla server URL (around line 728):

```javascript
// OLD (public server):
const VALHALLA_SERVER = 'https://valhalla1.openstreetmap.de';

// NEW (local server):
const VALHALLA_SERVER = 'http://localhost:8002';
```

### API Compatibility

The local server uses the **same API** as the public Valhalla server:
- All costing models work identically
- Request/response formats are the same
- No API keys required
- No rate limits

---

## 📝 Next Steps

### Immediate (After Tile Build Completes)

1. **Verify tiles complete** - Check all `.bin` files are finalized
2. **Create tile extract** (optional, improves load time):
   ```bash
   valhalla_build_extract -c config/valhalla_build.json -v
   ```
3. **Build admin boundaries** (optional):
   ```bash
   valhalla_build_admins -c config/valhalla_build.json
   ```
4. **Start the server**:
   ```bash
   valhalla_service config/valhalla.json 1
   ```
5. **Test routing**:
   ```bash
   curl "http://localhost:8002/route?json={\"locations\":[{\"lat\":-6.2088,\"lon\":106.8456},{\"lat\":-6.9175,\"lon\":107.6191}],\"costing\":\"auto\"}" | jq '.'
   ```

### Integration

6. **Update app** - Change `VALHALLA_SERVER` in `route-hotspots-valhalla-phase1.html`:
   ```javascript
   const VALHALLA_SERVER = 'http://localhost:8002';  // Was: valhalla1.openstreetmap.de
   ```

7. **Test Phase 1** - Verify Jakarta→Bandung routes work correctly

8. **Phase 2** - Integrate HERE Traffic Flow API (when ready)

---

## 📞 References

- **Valhalla GitHub:** https://github.com/valhalla/valhalla
- **Valhalla Docs:** https://valhalla.github.io/valhalla
- **OSM Indonesia:** https://download.geofabrik.de/asia/indonesia.html
- **This Setup Log:** `/home/ubuntu/.openclaw/workspace/memory/valhalla-build.log`

---

**Build Date:** 2026-03-12
**Valhalla Version:** 3.6.3
**Platform:** Ubuntu 24.04.4 LTS (ARM64)
**OSM Data:** Indonesia extract (1.6 GB)
**Tile Build Time:** ~1-2 hours (native ARM64)
