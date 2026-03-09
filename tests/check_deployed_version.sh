#!/bin/bash

# Script to check server version and status
# Usage: ./check_deployed_version.sh [local|production]

ENV=${1:-production}

if [ "$ENV" = "local" ]; then
    URL="http://localhost:5000/status"
    echo "Checking LOCAL server version..."
elif [ "$ENV" = "production" ] || [ "$ENV" = "prod" ]; then
    URL="https://learning-render-ut2u.onrender.com/status"
    echo "Checking PRODUCTION server version..."
else
    echo "Usage: $0 [local|production]"
    exit 1
fi

echo "URL: $URL"
echo ""

# Make the request
response=$(curl -s "$URL")

# Check if jq is available for pretty printing
if command -v jq &> /dev/null; then
    echo "$response" | jq '.'
else
    # Fallback: pretty print without jq
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
fi

# Extract and highlight version info if jq is available
if command -v jq &> /dev/null; then
    echo ""
    echo "=== VERSION INFO ==="
    echo "Commit ID:      $(echo "$response" | jq -r '.version.commit_id')"
    echo "Commit Time:    $(echo "$response" | jq -r '.version.commit_time')"
    echo "Commit Message: $(echo "$response" | jq -r '.version.commit_message')"
fi
