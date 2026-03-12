#!/bin/bash
# 03-start-server.sh - Start Valhalla routing server
# Starts Docker container with Jabodetabek tiles

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
CONFIG_DIR="$SCRIPT_DIR/config"
TILES_DIR="$DATA_DIR/tiles"

echo "=== Valhalla Jabodetabek - Start Server ==="
echo ""

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found!"
    exit 1
fi

if [ ! -d "$TILES_DIR/tiles" ]; then
    echo "✗ Tiles not found!"
    echo "  Please run ./02-build-tiles.sh first"
    exit 1
fi

# Check if container is already running
if docker ps | grep -q valhalla-jabodetabek; then
    echo "⚠ Valhalla server is already running"
    echo ""
    echo "Options:"
    echo "  1. Restart: docker restart valhalla-jabodetabek"
    echo "  2. Stop first: ./04-stop-server.sh then run this script"
    echo "  3. View logs: ./05-view-logs.sh"
    exit 0
fi

echo "Starting Valhalla server..."
echo ""

# Create runtime configuration
cat > "$CONFIG_DIR/valhalla_runtime.json" << EOF
{
  "service_limits": {
    "max_alternatives": 5,
    "max_route_length": 500000,
    "max_matrix_time": 600
  },
  "tile_extract": {
    "tile_dir": "/data/tiles/tiles"
  },
  "locality": {
    "locale_file": "/data/locale/locality.json"
  },
  "time_zone": {
    "time_zone_file": "/data/timezone/time_zones.json"
  },
  "elevation": {
    "elevation_data_dir": "/data/elevation"
  },
  "meili": {
    "turn_penalty_factor": 30,
    "breakage_distance": 50,
    "interpolation_distance": 10
  },
  "http_service": {
    "listening_port": 8002,
    "address": "0.0.0.0"
  }
}
EOF

# Start Docker container
sudo docker run -d \
  --name valhalla-jabodetabek \
  --platform linux/amd64 \
  -p 8002:8002 \
  -v "$DATA_DIR:/data" \
  -v "$CONFIG_DIR/valhalla_runtime.json:/valhalla.json" \
  --restart unless-stopped \
  valhalla/valhalla:run-latest

echo ""
echo "Waiting for server to start..."
sleep 5

# Check if server is running
if docker ps | grep -q valhalla-jabodetabek; then
    echo "✓ Valhalla server started successfully!"
    echo ""
    echo "Server details:"
    echo "  - Local: http://localhost:8002"
    echo "  - Status: http://localhost:8002/status"
    echo "  - Route API: http://localhost:8002/route"
    echo ""
    echo "Update your app:"
    echo "  Edit route-hotspots-valhalla-phase1.html"
    echo "  Change: const VALHALLA_SERVER = 'http://localhost:8002';"
    echo ""
    echo "Management commands:"
    echo "  - Stop: ./04-stop-server.sh"
    echo "  - Logs: ./05-view-logs.sh"
    echo "  - Restart: docker restart valhalla-jabodetabek"
else
    echo "✗ Server failed to start"
    echo ""
    echo "Check logs:"
    echo "  ./05-view-logs.sh"
    echo "  or: docker logs valhalla-jabodetabek"
    exit 1
fi
