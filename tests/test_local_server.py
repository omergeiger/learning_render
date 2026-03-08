#!/usr/bin/env python3
"""
Local Server Test Script
Tests the Flask server running on localhost

Usage:
    python test_local_server.py
"""

import requests
import sys
from datetime import datetime

# Configuration
SERVER_URL = "http://localhost:5000"
TIMEOUT = 5  # seconds
VERIFY_TOKEN = "!QAZxsw2"  # Your webhook verify token


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
    """Test 1: GET /status endpoint"""
    print_header("Test 1: GET /status endpoint")

    endpoint = f"{SERVER_URL}/status"
    print(f"URL: {endpoint}")

    try:
        response = requests.get(endpoint, timeout=TIMEOUT)

        status_ok = response.status_code == 200
        print_test("HTTP Status Code", status_ok, f"Got {response.status_code}")

        if status_ok:
            data = response.json()
            print_test("Response is JSON", True)
            print_test("Has 'status' field", 'status' in data, f"Value: {data.get('status')}")
            print_test("Has 'timestamp' field", 'timestamp' in data)
            print_test("Has 'message' field", 'message' in data)

            print(f"\n📄 Response: {data}")
            return True
        return False

    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Server not running? Start with: python app.py")
        return False
    except Exception as e:
        print_test("Request", False, f"Error: {e}")
        return False


def test_write_endpoint():
    """Test 2: POST /write endpoint (echo)"""
    print_header("Test 2: POST /write endpoint (echo)")

    endpoint = f"{SERVER_URL}/write"
    print(f"URL: {endpoint}")

    test_text = "Testing local server!"
    payload = {"text": test_text}

    try:
        response = requests.post(endpoint, json=payload, timeout=TIMEOUT)

        status_ok = response.status_code == 200
        print_test("HTTP Status Code", status_ok, f"Got {response.status_code}")

        if status_ok:
            data = response.json()
            print_test("Response is JSON", True)

            echo_match = data.get('echo') == test_text
            print_test("Echo matches input", echo_match, f"Echo: '{data.get('echo')}'")

            length_ok = data.get('length') == len(test_text)
            print_test("Length is correct", length_ok, f"Got: {data.get('length')}")

            has_timestamp = 'timestamp' in data
            print_test("Has timestamp", has_timestamp)

            print(f"\n📄 Response: {data}")
            return echo_match and length_ok and has_timestamp
        return False

    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Server not running?")
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


def main():
    """Run all tests"""
    print("\n")
    print("🧪 LOCAL SERVER TEST SUITE")
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
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
        print("   cd /Users/ogeiger/git/learning_render")
        print("   source .venv/bin/activate")
        print("   python app.py")
        return 1
    except Exception as e:
        print_test("Server is reachable", False, f"Error: {e}")
        return 1

    # Run all tests
    results = {
        "Test 1: Status Endpoint": test_status_endpoint(),
        "Test 2: Write Endpoint": test_write_endpoint(),
        "Test 3: Webhook Verification (Success)": test_webhook_verification_success(),
        "Test 4: Webhook Verification (Failure)": test_webhook_verification_failure(),
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
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
