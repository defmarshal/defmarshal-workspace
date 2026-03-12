#!/bin/bash
# 01-download-osm.sh - Download OSM data for Jabodetabek
# Options: BBBike extracts or custom bounding box

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
CONFIG_DIR="$SCRIPT_DIR/config"

# Create directories
mkdir -p "$DATA_DIR"
mkdir -p "$CONFIG_DIR"

echo "=== Valhalla Jabodetabek - OSM Data Download ==="
echo ""

# Define Jabodetabek bounding box
# West: 106.529 (Tangerang west)
# South: -6.714 (Bogor south)
# East: 107.097 (Bekasi east)
# North: -6.014 (Jakarta north)
JABODETABEK_BOUNDS="106.529,-6.714,107.097,-6.014"

# Save bounding box to config
echo "$JABODETABEK_BOUNDS" > "$CONFIG_DIR/jabodetabek.bounds"
echo "✓ Saved bounding box to config/jabodetabek.bounds"
echo "  Bounds: $JABODETABEK_BOUNDS"
echo ""

# Option 1: Download from BBBike (Jakarta metro extract)
echo "Downloading OSM data from BBBike..."
echo "  Source: https://download.bbbike.org/osm/bbbike/Jakarta/"
echo ""

cd "$DATA_DIR"

# Check if wget or curl is available
if command -v wget &> /dev/null; then
    DOWNLOAD_CMD="wget -q --show-progress"
elif command -v curl &> /dev/null; then
    DOWNLOAD_CMD="curl -L -o jakarta.osm.pbf"
else
    echo "ERROR: Neither wget nor curl found. Please install one."
    exit 1
fi

# Download Jakarta metro (covers most of Jabodetabek)
echo "Downloading Jakarta metro extract (~50-100 MB)..."
$DOWNLOAD_CMD https://download.bbbike.org/osm/bbbike/Jakarta/Jakarta-latest.osm.pbf

if [ -f "Jakarta/Jakarta-latest.osm.pbf" ]; then
    # BBBike extracts to subdirectory
    mv Jakarta/Jakarta-latest.osm.pbf jakarta-latest.osm.pbf
    rm -rf Jakarta
fi

if [ -f "jakarta-latest.osm.pbf" ]; then
    echo ""
    echo "✓ Download complete: $(ls -lh jakarta-latest.osm.pbf | awk '{print $5}')"
    
    # Optional: Download surrounding areas for better coverage
    echo ""
    echo "Optional: Download surrounding areas for better coverage?"
    echo "  - Bogor: extends coverage south"
    echo "  - Tangerang: extends coverage west"
    echo "  - Bekasi: extends coverage east"
    echo ""
    read -p "Download additional areas? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Downloading Bogor..."
        $DOWNLOAD_CMD https://download.bbbike.org/osm/bbbike/Bogor/Bogor-latest.osm.pbf 2>/dev/null || echo "  (skipped)"
        
        echo "Downloading Tangerang..."
        $DOWNLOAD_CMD https://download.bbbike.org/osm/bbbike/Tangerang/Tangerang-latest.osm.pbf 2>/dev/null || echo "  (skipped)"
        
        echo "Downloading Bekasi..."
        $DOWNLOAD_CMD https://download.bbbike.org/osm/bbbike/Bekasi/Bekasi-latest.osm.pbf 2>/dev/null || echo "  (skipped)"
        
        # Merge if multiple files exist
        MERGE_FILES="jakarta-latest.osm.pbf"
        [ -f "Bogor-latest.osm.pbf" ] && MERGE_FILES="$MERGE_FILES Bogor-latest.osm.pbf"
        [ -f "Tangerang-latest.osm.pbf" ] && MERGE_FILES="$MERGE_FILES Tangerang-latest.osm.pbf"
        [ -f "Bekasi-latest.osm.pbf" ] && MERGE_FILES="$MERGE_FILES Bekasi-latest.osm.pbf"
        
        if [ $(echo $MERGE_FILES | wc -w) -gt 1 ]; then
            echo ""
            echo "Merging files..."
            if command -v osmium &> /dev/null; then
                osmium merge $MERGE_FILES -o jabodetabek.osm.pbf
                echo "✓ Merged to jabodetabek.osm.pbf"
            else
                echo "⚠ osmium not found. Install with: sudo apt install osmium-tool"
                echo "  Using Jakarta data only for now."
                cp jakarta-latest.osm.pbf jabodetabek.osm.pbf
            fi
        else
            cp jakarta-latest.osm.pbf jabodetabek.osm.pbf
        fi
    else
        # Just use Jakarta data
        cp jakarta-latest.osm.pbf jabodetabek.osm.pbf
    fi
    
    echo ""
    echo "✓ Final OSM file: $(ls -lh jabodetabek.osm.pbf | awk '{print $5}')"
    echo ""
    echo "=== Download Complete ==="
    echo ""
    echo "Next step: Run ./02-build-tiles.sh to build Valhalla tiles"
    echo "  This will take 1-2 hours depending on your hardware."
else
    echo ""
    echo "✗ Download failed!"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check your internet connection"
    echo "  2. Try manual download: wget https://download.bbbike.org/osm/bbbike/Jakarta/Jakarta-latest.osm.pbf"
    echo "  3. Use alternative source: Geofabrik Indonesia"
    echo ""
    exit 1
fi
