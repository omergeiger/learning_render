#!/bin/bash
#
# Spawn local Flask development server
# Usage: ./spawn_local_server.sh [port]
#

set -e

# Default port
PORT=${1:-5000}

# Get project root (two levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# PID file location
PID_FILE="/tmp/flask_local_server_${PORT}.pid"

cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found at .venv"
    echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if port is already in use
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Error: Port $PORT is already in use"
    echo "Run: ./tests/local/kill_local_server.sh $PORT"
    exit 1
fi

# Check if server is already running (PID file exists and process is alive)
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Error: Server already running with PID $OLD_PID on port $PORT"
        echo "Run: ./tests/local/kill_local_server.sh $PORT"
        exit 1
    else
        # Clean up stale PID file
        rm -f "$PID_FILE"
    fi
fi

echo "Starting Flask server on port $PORT..."

# Start server in background
source .venv/bin/activate
PORT=$PORT python3 app.py > /tmp/flask_local_server_${PORT}.log 2>&1 &
SERVER_PID=$!

# Save PID
echo "$SERVER_PID" > "$PID_FILE"

echo "Server starting with PID $SERVER_PID"
echo "Waiting for server to be ready..."

# Wait for server to be ready (max 10 seconds)
COUNTER=0
MAX_ATTEMPTS=20
while [ $COUNTER -lt $MAX_ATTEMPTS ]; do
    if curl -s "http://localhost:${PORT}/status" > /dev/null 2>&1; then
        echo "✅ Server is ready on http://localhost:${PORT}"
        echo "PID: $SERVER_PID (saved to $PID_FILE)"
        echo "Logs: /tmp/flask_local_server_${PORT}.log"
        exit 0
    fi
    sleep 0.5
    COUNTER=$((COUNTER + 1))
done

echo "❌ Server failed to start within 10 seconds"
echo "Check logs: cat /tmp/flask_local_server_${PORT}.log"

# Clean up
kill "$SERVER_PID" 2>/dev/null || true
rm -f "$PID_FILE"
exit 1
