#!/bin/bash
# 02-build-tiles.sh - Build Valhalla tiles for Jabodetabek
# This script builds routing tiles from OSM data
# Estimated time: 1-2 hours

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
CONFIG_DIR="$SCRIPT_DIR/config"
TILES_DIR="$DATA_DIR/tiles"

echo "=== Valhalla Jabodetabek - Build Tiles ==="
echo ""

# Check prerequisites
if [ ! -f "$DATA_DIR/jabodetabek.osm.pbf" ]; then
    echo "✗ OSM data not found!"
    echo "  Please run ./01-download-osm.sh first"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found!"
    echo "  Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ OSM data found: $(ls -lh $DATA_DIR/jabodetabek.osm.pbf | awk '{print $5}')"
echo "✓ Docker found: $(docker --version)"
echo ""

# Create tiles directory
mkdir -p "$TILES_DIR"

# Clean old tiles
echo "Cleaning old tiles..."
rm -rf "$TILES_DIR"/*
mkdir -p "$TILES_DIR"/{tiles,elevation,locale,timezone}

# Read bounding box
if [ -f "$CONFIG_DIR/jabodetabek.bounds" ]; then
    BOUNDS=$(cat "$CONFIG_DIR/jabodetabek.bounds")
    echo "✓ Bounding box: $BOUNDS"
else
    # Default Jabodetabek bounds
    BOUNDS="106.529,-6.714,107.097,-6.014"
    echo "⚠ Using default bounds: $BOUNDS"
fi
echo ""

# Create Valhalla configuration
echo "Creating Valhalla configuration..."
cat > "$CONFIG_DIR/valhalla_build.json" << 'EOF'
{
  "mjolnir": {
    "tile_dir": "/data/tiles/tiles",
    "planet_file": "/data/jabodetabek.osm.pbf",
    "use_hierarchy": false,
    "exclude_unpaved": false
  },
  "locality": {
    "locale_file": "/data/locale/locality.json"
  },
  "time_zone": {
    "time_zone_file": "/data/timezone/time_zones.json"
  },
  "elevation": {
    "elevation_data_dir": "/data/elevation"
  }
}
EOF

# Create locality configuration (Indonesia)
cat > "$CONFIG_DIR/locality.json" << 'EOF'
{
  "localities": [
    {
      "name": "ID",
      "drive_on_right": false,
      "internal": false
    }
  ]
}
EOF

# Copy config files to data directory
cp "$CONFIG_DIR/locality.json" "$DATA_DIR/locale/"

echo "✓ Configuration created"
echo ""

# Run Valhalla tile builder using Docker
echo "=== Building Tiles ==="
echo "This will take 1-2 hours. Progress will be shown below."
echo ""

sudo docker run --rm --platform linux/amd64 \
  -v "$DATA_DIR:/data" \
  -v "$CONFIG_DIR/valhalla_build.json:/valhalla_build.json" \
  valhalla/valhalla:run-latest \
  valhalla_build_tiles -c /valhalla_build.json /data/jabodetabek.osm.pbf

echo ""
echo "✓ Tile building complete"
echo ""

# Create tile extract
echo "=== Creating Tile Extract ==="
echo ""

sudo docker run --rm --platform linux/amd64 \
  -v "$DATA_DIR:/data" \
  -v "$CONFIG_DIR/valhalla_build.json:/valhalla_build.json" \
  valhalla/valhalla:run-latest \
  valhalla_build_extract -c /valhalla_build.json

echo ""
echo "✓ Tile extraction complete"
echo ""

# Build elevation data (optional but recommended)
echo "=== Building Elevation Data ==="
echo "This adds ~15-30 minutes but improves routing accuracy"
echo ""

sudo docker run --rm --platform linux/amd64 \
  -v "$DATA_DIR:/data" \
  valhalla/valhalla:run-latest \
  valhalla_build_elevation --threads 2

echo ""
echo "✓ Elevation data built"
echo ""

# Verify tiles
echo "=== Verifying Build ==="
TILE_COUNT=$(find "$TILES_DIR/tiles" -name "*.gph" 2>/dev/null | wc -l)
echo "✓ Generated $TILE_COUNT tile files"

if [ $TILE_COUNT -gt 0 ]; then
    echo ""
    echo "=== Build Complete ==="
    echo ""
    echo "Tile directory: $TILES_DIR"
    echo "Total size: $(du -sh $TILES_DIR | awk '{print $1}')"
    echo ""
    echo "Next step: Run ./03-start-server.sh to start the routing server"
else
    echo ""
    echo "✗ Build may have failed - no tiles generated"
    echo "  Check the output above for errors"
    exit 1
fi
