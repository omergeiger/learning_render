#!/bin/bash
#
# Master local testing script
# Spawns server, runs all tests, and cleans up
# Usage: ./test_locally.sh [port]
#

set -e

# Default port
PORT=${1:-5000}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "🧪 Local Testing Suite"
echo "========================================"
echo "Port: $PORT"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Cleanup function
cleanup() {
    echo ""
    echo "========================================"
    echo "🧹 Cleaning up..."
    echo "========================================"
    "$SCRIPT_DIR/kill_local_server.sh" "$PORT"

    echo ""
    echo "========================================"
    echo "📊 Test Summary"
    echo "========================================"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}✅ All tests passed!${NC}"
        exit 0
    else
        echo -e "\n${RED}❌ Some tests failed${NC}"
        exit 1
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Step 1: Spawn server
echo "========================================"
echo "🚀 Step 1: Starting local server"
echo "========================================"
if "$SCRIPT_DIR/spawn_local_server.sh" "$PORT"; then
    echo -e "${GREEN}✅ Server started${NC}"
else
    echo -e "${RED}❌ Failed to start server${NC}"
    exit 1
fi

echo ""

# Step 2: Test status endpoint
echo "========================================"
echo "🔍 Step 2: Testing /status endpoint"
echo "========================================"
if "$SCRIPT_DIR/test_local_status.sh" "$PORT"; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}✅ Status endpoint test passed${NC}"
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}❌ Status endpoint test failed${NC}"
fi

echo ""

# Step 3: Run Python test suite
echo "========================================"
echo "🐍 Step 3: Running Python test suite"
echo "========================================"

# Get project root
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Activate virtual environment and run tests
cd "$PROJECT_ROOT"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    if python3 "$SCRIPT_DIR/test_local_server.py" --port "$PORT"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✅ Python test suite passed${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}❌ Python test suite failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Virtual environment not found, skipping Python tests${NC}"
fi

# Cleanup will be called by trap
