#!/bin/bash
# 04-stop-server.sh - Stop Valhalla routing server

echo "=== Valhalla Jabodetabek - Stop Server ==="
echo ""

# Check if container exists
if ! sudo docker ps -a | grep -q valhalla-jabodetabek; then
    echo "⚠ Valhalla server container not found"
    echo "  Nothing to stop"
    exit 0
fi

# Stop container
echo "Stopping Valhalla server..."
sudo docker stop valhalla-jabodetabek

echo ""
echo "✓ Server stopped"
echo ""
echo "To start again: ./03-start-server.sh"
