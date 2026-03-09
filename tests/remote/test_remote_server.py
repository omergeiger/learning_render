#!/usr/bin/env python3
"""
Remote Server Health Test Script
Tests the deployed Flask server on Render.com

Usage:
    python test_remote_server.py [--url URL]

Examples:
    python test_remote_server.py
    python test_remote_server.py --url https://learning-render-ut2u.onrender.com
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
DEFAULT_SERVER_URL = "https://learning-render-ut2u.onrender.com"
TIMEOUT = 20  # seconds
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
    """Test GET /status endpoint (health check + version info)"""
    print_header("Testing GET /status endpoint")

    endpoint = f"{SERVER_URL}/status"
    print(f"URL: {endpoint}")

    try:
        # Make request
        response = requests.get(endpoint, timeout=TIMEOUT)

        # Check status code
        status_ok = response.status_code == 200
        print_test(
            "HTTP Status Code",
            status_ok,
            f"Got {response.status_code}, expected 200"
        )

        if not status_ok:
            return False

        # Check response is JSON
        try:
            data = response.json()
            print_test("Response is valid JSON", True)
        except ValueError:
            print_test("Response is valid JSON", False, "Invalid JSON response")
            return False

        # Check required fields
        required_fields = ['status', 'timestamp', 'message']
        for field in required_fields:
            has_field = field in data
            print_test(
                f"Has '{field}' field",
                has_field,
                f"Value: {data.get(field, 'N/A')}"
            )

        # Check status value
        print_test(
            "Status is 'ok'",
            data.get('status') == 'ok',
            f"Got: {data.get('status')}"
        )

        # Validate timestamp format (ISO 8601)
        timestamp = data.get('timestamp', '')
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            print_test("Timestamp is valid ISO format", True, timestamp)
        except ValueError:
            print_test("Timestamp is valid ISO format", False, f"Invalid: {timestamp}")

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

        print("\n📄 Full Response:")
        print(f"   {data}")

        return all_checks_pass

    except requests.exceptions.Timeout:
        print_test("Request completed", False, f"Timeout after {TIMEOUT}s")
        return False
    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Could not connect to server")
        return False
    except Exception as e:
        print_test("Request completed", False, f"Error: {str(e)}")
        return False


def test_webhook_verification_success():
    """Test GET /webhook - Successful verification"""
    print_header("Testing Webhook Verification (SUCCESS)")

    endpoint = f"{SERVER_URL}/webhook"
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': VERIFY_TOKEN,
        'hub.challenge': 'challenge_test_12345'
    }

    print(f"URL: {endpoint}")
    print(f"Simulating Meta's verification request")

    try:
        response = requests.get(endpoint, params=params, timeout=TIMEOUT)

        # Should return 200
        status_ok = response.status_code == 200
        print_test(
            "HTTP Status Code is 200",
            status_ok,
            f"Got {response.status_code}"
        )

        # Should return the challenge string
        challenge_returned = response.text == 'challenge_test_12345'
        print_test(
            "Returns challenge string",
            challenge_returned,
            f"Got: '{response.text[:50]}...'" if len(response.text) > 50 else f"Got: '{response.text}'"
        )

        if status_ok and challenge_returned:
            print("\n✅ Webhook verification would succeed with Meta")
            return True

        return False

    except Exception as e:
        print_test("Webhook verification test", False, f"Error: {str(e)}")
        return False


def test_webhook_verification_failure():
    """Test GET /webhook - Failed verification (wrong token)"""
    print_header("Testing Webhook Verification (FAILURE)")

    endpoint = f"{SERVER_URL}/webhook"
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': 'wrong_token_should_fail',
        'hub.challenge': 'challenge_test_12345'
    }

    print(f"URL: {endpoint}")
    print(f"Testing with wrong verify token (security check)")

    try:
        response = requests.get(endpoint, params=params, timeout=TIMEOUT)

        # Should return 403 Forbidden
        is_403 = response.status_code == 403
        print_test(
            "HTTP Status Code is 403",
            is_403,
            f"Got {response.status_code}"
        )

        is_forbidden = response.text == 'Forbidden'
        print_test(
            "Returns 'Forbidden'",
            is_forbidden,
            f"Got: '{response.text}'"
        )

        if is_403 and is_forbidden:
            print("\n✅ Security working - wrong token rejected")
            return True

        return False

    except Exception as e:
        print_test("Webhook security test", False, f"Error: {str(e)}")
        return False


def main(server_url=None):
    """Run all tests"""
    global SERVER_URL
    SERVER_URL = server_url or DEFAULT_SERVER_URL

    print("\n")
    print("🧪 REMOTE SERVER HEALTH TEST")
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    print(f"🔑 Verify Token: {VERIFY_TOKEN}")
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "Status Endpoint": test_status_endpoint(),
        "Webhook Verification (Success)": test_webhook_verification_success(),
        "Webhook Verification (Failure)": test_webhook_verification_failure(),
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
        print("✅ Server is healthy and functioning correctly")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Server may have issues - check logs")
        return 1


if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Test remote production server')
        parser.add_argument('--url', type=str, help=f'Server URL (default: {DEFAULT_SERVER_URL})')
        args = parser.parse_args()

        exit_code = main(server_url=args.url)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
