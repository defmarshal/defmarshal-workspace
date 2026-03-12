#!/bin/bash
# 05-view-logs.sh - View Valhalla server logs

echo "=== Valhalla Jabodetabek - Server Logs ==="
echo ""
echo "Press Ctrl+C to exit"
echo ""

# Check if container exists
if ! sudo docker ps -a | grep -q valhalla-jabodetabek; then
    echo "⚠ Valhalla server container not found"
    echo "  Start the server first: ./03-start-server.sh"
    exit 1
fi

# Show logs
sudo docker logs -f valhalla-jabodetabek
