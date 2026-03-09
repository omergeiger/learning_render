#!/bin/bash
#
# Kill local Flask development server gracefully
# Usage: ./kill_local_server.sh [port]
#

# Default port
PORT=${1:-5000}

# PID file location
PID_FILE="/tmp/flask_local_server_${PORT}.pid"
LOG_FILE="/tmp/flask_local_server_${PORT}.log"

if [ ! -f "$PID_FILE" ]; then
    echo "No PID file found for port $PORT"
    echo "Attempting to kill any process on port $PORT..."

    # Try to find and kill process using the port
    PID=$(lsof -ti:"$PORT" 2>/dev/null)
    if [ -n "$PID" ]; then
        echo "Found process $PID on port $PORT, killing..."
        kill "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null
        echo "✅ Process killed"
    else
        echo "No process found on port $PORT"
    fi
    exit 0
fi

# Read PID from file
SERVER_PID=$(cat "$PID_FILE")

# Check if process is running
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo "Stopping server with PID $SERVER_PID on port $PORT..."

    # Try graceful shutdown first (SIGTERM)
    kill "$SERVER_PID" 2>/dev/null

    # Wait up to 5 seconds for graceful shutdown
    COUNTER=0
    while [ $COUNTER -lt 10 ]; do
        if ! ps -p "$SERVER_PID" > /dev/null 2>&1; then
            echo "✅ Server stopped gracefully"
            rm -f "$PID_FILE"
            rm -f "$LOG_FILE"
            exit 0
        fi
        sleep 0.5
        COUNTER=$((COUNTER + 1))
    done

    # Force kill if still running (SIGKILL)
    echo "Server didn't stop gracefully, force killing..."
    kill -9 "$SERVER_PID" 2>/dev/null
    echo "✅ Server force stopped"
else
    echo "Server PID $SERVER_PID is not running (stale PID file)"
fi

# Clean up PID file and log
rm -f "$PID_FILE"
rm -f "$LOG_FILE"
echo "Cleaned up PID file and logs"
