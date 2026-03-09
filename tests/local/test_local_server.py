#!/usr/bin/env python3
"""
Local Server Test Script
Tests the Flask server running on localhost

Usage:
    python test_local_server.py [--port PORT]

Examples:
    python test_local_server.py
    python test_local_server.py --port 5001
"""

import requests
import sys
import argparse
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TIMEOUT = 5  # seconds
VERIFY_TOKEN = os.getenv('META_WA_VERIFY_TOKEN', 'abc123')  # Get from .env or default


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_test(name, status, details=""):
    """Print test result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   └─ {details}")


def test_status_endpoint():
    """Test 1: GET /status endpoint (health check + version info)"""
    print_header("Test 1: GET /status endpoint")

    endpoint = f"{SERVER_URL}/status"
    print(f"URL: {endpoint}")

    try:
        response = requests.get(endpoint, timeout=TIMEOUT)

        status_ok = response.status_code == 200
        print_test("HTTP Status Code", status_ok, f"Got {response.status_code}")

        if not status_ok:
            return False

        data = response.json()
        print_test("Response is JSON", True)

        # Check basic fields
        print_test("Has 'status' field", 'status' in data, f"Value: {data.get('status')}")
        print_test("Has 'timestamp' field", 'timestamp' in data)
        print_test("Has 'message' field", 'message' in data)

        # Check version info
        has_version = 'version' in data
        print_test("Has 'version' field", has_version)

        all_checks_pass = True
        if has_version:
            version = data['version']
            has_commit_id = 'commit_id' in version
            has_commit_time = 'commit_time' in version
            has_commit_msg = 'commit_message' in version

            print_test("Has commit_id", has_commit_id, f"Value: {version.get('commit_id')}")
            print_test("Has commit_time", has_commit_time, f"Value: {version.get('commit_time')}")
            print_test("Has commit_message", has_commit_msg, f"Value: {version.get('commit_message')}")

            all_checks_pass = has_commit_id and has_commit_time and has_commit_msg
        else:
            all_checks_pass = False

        print(f"\n📄 Response: {data}")
        return all_checks_pass

    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Server not running? Start with: python app.py")
        return False
    except Exception as e:
        print_test("Request", False, f"Error: {e}")
        return False


def test_webhook_verification_success():
    """Test 3: GET /webhook - Successful verification"""
    print_header("Test 3: Webhook Verification (SUCCESS)")

    endpoint = f"{SERVER_URL}/webhook"
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': VERIFY_TOKEN,
        'hub.challenge': 'test123'
    }

    print(f"URL: {endpoint}")
    print(f"Params: {params}")

    try:
        response = requests.get(endpoint, params=params, timeout=TIMEOUT)

        status_ok = response.status_code == 200
        print_test("HTTP Status Code", status_ok, f"Got {response.status_code}")

        # Response should be the challenge string
        challenge_returned = response.text == 'test123'
        print_test("Returns challenge", challenge_returned, f"Got: '{response.text}'")

        if status_ok and challenge_returned:
            print("\n✅ Webhook verification would succeed with Meta")
            return True
        return False

    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Server not running?")
        return False
    except Exception as e:
        print_test("Request", False, f"Error: {e}")
        return False


def test_webhook_verification_failure():
    """Test 4: GET /webhook - Failed verification (wrong token)"""
    print_header("Test 4: Webhook Verification (FAILURE)")

    endpoint = f"{SERVER_URL}/webhook"
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': 'wrong_token',
        'hub.challenge': 'test123'
    }

    print(f"URL: {endpoint}")
    print(f"Params: {params}")

    try:
        response = requests.get(endpoint, params=params, timeout=TIMEOUT)

        # Should return 403 Forbidden
        is_403 = response.status_code == 403
        print_test("HTTP Status Code is 403", is_403, f"Got {response.status_code}")

        is_forbidden = response.text == 'Forbidden'
        print_test("Returns 'Forbidden'", is_forbidden, f"Got: '{response.text}'")

        if is_403 and is_forbidden:
            print("\n✅ Security working - wrong token rejected")
            return True
        return False

    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Server not running?")
        return False
    except Exception as e:
        print_test("Request", False, f"Error: {e}")
        return False


def main(port=5000):
    """Run all tests"""
    global SERVER_URL
    SERVER_URL = f"http://localhost:{port}"

    print("\n")
    print("🧪 LOCAL SERVER TEST SUITE")
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    print(f"🔑 Verify Token: {VERIFY_TOKEN}")
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check if server is reachable first
    print_header("Checking Server Connectivity")
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=2)
        print_test("Server is reachable", True, f"Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_test("Server is reachable", False, "Connection refused")
        print("\n❌ ERROR: Server is not running!")
        print("\n💡 To start the server, run:")
        print(f"   ./tests/local/spawn_local_server.sh {port}")
        return 1
    except Exception as e:
        print_test("Server is reachable", False, f"Error: {e}")
        return 1

    # Run all tests
    results = {
        "Test 1: Status Endpoint": test_status_endpoint(),
        "Test 2: Webhook Verification (Success)": test_webhook_verification_success(),
        "Test 3: Webhook Verification (Failure)": test_webhook_verification_failure(),
    }

    # Summary
    print_header("TEST SUMMARY")

    all_passed = all(results.values())

    for test_name, passed in results.items():
        symbol = "✅" if passed else "❌"
        status = "PASSED" if passed else "FAILED"
        print(f"{symbol} {test_name}: {status}")

    print("\n" + "=" * 60)

    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Local server is healthy and ready for deployment")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Fix issues before deploying")
        return 1


if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Test local Flask server')
        parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
        args = parser.parse_args()

        exit_code = main(port=args.port)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
