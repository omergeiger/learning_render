#!/bin/bash
#
# Test local Flask server /status endpoint
# Usage: ./test_local_status.sh [port]
#

set -e

# Default port
PORT=${1:-5000}
URL="http://localhost:${PORT}/status"

echo "Testing GET $URL"
echo "======================================"

# Make request
RESPONSE=$(curl -s "$URL")

# Check if jq is available for pretty printing
if command -v jq &> /dev/null; then
    echo "$RESPONSE" | jq '.'

    # Extract and highlight version info
    echo ""
    echo "=== VERSION INFO ==="
    echo "Commit ID:      $(echo "$RESPONSE" | jq -r '.version.commit_id')"
    echo "Commit Time:    $(echo "$RESPONSE" | jq -r '.version.commit_time')"
    echo "Commit Message: $(echo "$RESPONSE" | jq -r '.version.commit_message')"
    echo ""
    echo "=== STATUS ==="
    echo "Status:         $(echo "$RESPONSE" | jq -r '.status')"
    echo "Message:        $(echo "$RESPONSE" | jq -r '.message')"
else
    # Fallback: pretty print without jq
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
fi

# Validate response
STATUS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', ''))" 2>/dev/null)

if [ "$STATUS" = "ok" ]; then
    echo ""
    echo "✅ Status check PASSED"
    exit 0
else
    echo ""
    echo "❌ Status check FAILED: status != 'ok'"
    exit 1
fi
