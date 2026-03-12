# Valhalla Routing Server - Jabodetabek

Self-hosted Valhalla routing engine for Jabodetabek area (Jakarta, Bogor, Depok, Tangerang, Bekasi).

## Quick Start

### Prerequisites

- Docker installed
- At least 15 GB free disk space
- 4 GB RAM recommended
- Linux/macOS (WSL2 works on Windows)

### Setup (First Time - ~2 hours)

```bash
# 1. Clone/navigate to this directory
cd valhalla-jabodetabek

# 2. Make scripts executable
chmod +x *.sh

# 3. Download OSM data for Jabodetabek (~5-15 min)
./01-download-osm.sh

# 4. Build Valhalla tiles (~1-2 hours)
./02-build-tiles.sh

# 5. Start the server
./03-start-server.sh
```

### Update Your App

Edit `route-hotspots-valhalla-phase1.html`:

```javascript
// Change this line (around line 728):
const VALHALLA_SERVER = 'http://localhost:8002';  // or your server IP
```

### Test

Open your browser:
- `http://localhost:8002/status` - Server status
- Your app should now use local Valhalla server

---

## Daily Operations

### Start Server

```bash
./03-start-server.sh
```

### Stop Server

```bash
./04-stop-server.sh
```

### Check Logs

```bash
./05-view-logs.sh
```

### Update OSM Data (Monthly)

```bash
./01-download-osm.sh    # Re-download latest data
./02-build-tiles.sh     # Rebuild tiles
docker restart valhalla # Restart to load new tiles
```

---

## Directory Structure

```
valhalla-jabodetabek/
├── 01-download-osm.sh      # Download OSM data
├── 02-build-tiles.sh       # Build Valhalla tiles
├── 03-start-server.sh      # Start Docker container
├── 04-stop-server.sh       # Stop Docker container
├── 05-view-logs.sh         # View server logs
├── config/
│   ├── valhalla.json       # Valhalla configuration
│   └── jabodetabek.bounds  # Bounding box coordinates
├── data/
│   ├── jabodetabek.osm.pbf # OSM data (downloaded)
│   └── tiles/              # Valhalla tiles (generated)
└── docker/
    └── Dockerfile          # Custom Docker image (optional)
```

---

## Configuration

### Alternatives Settings

Edit `config/valhalla.json`:

```json
{
  "service_limits": {
    "max_alternatives": 5
  }
}
```

### Bounding Box

Edit `config/jabodetabek.bounds`:
```
106.529,-6.714,107.097,-6.014
```

Format: `minLon,minLat,maxLon,maxLat`

---

## Troubleshooting

### Server Won't Start

```bash
# Check if port 8002 is in use
lsof -i :8002

# Kill existing process or change port in 03-start-server.sh
```

### Out of Disk Space

```bash
# Clean up old tiles
rm -rf data/tiles/*

# Rebuild with fresh data
./02-build-tiles.sh
```

### Routes Not Found

1. Check server status: `curl http://localhost:8002/status`
2. View logs: `./05-view-logs.sh`
3. Verify OSM data covers your area

---

## Performance Tips

1. **Use SSD storage** - Tile loading is I/O intensive
2. **Allocate more RAM** - 8 GB recommended for better caching
3. **Enable elevation** - More accurate routing (adds ~1 GB)
4. **Tune alternatives** - Balance quality vs. speed

---

## Resources

- [Valhalla Documentation](https://valhalla.github.io/valhalla/)
- [OSM Jabodetabek](https://download.bbbike.org/osm/bbbike/Jakarta/)
- [Docker Hub - Valhalla](https://hub.docker.com/r/valhalla/valhalla)
