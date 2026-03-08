#!/usr/bin/env python3
"""
Remote Server Health Test Script
Tests the deployed Flask server on Render.com

Usage:
    python test_remote_server.py
"""

import requests
import sys
from datetime import datetime

# Configuration
SERVER_URL = "https://learning-render-ut2u.onrender.com"
TIMEOUT = 10  # seconds
VERIFY_TOKEN = "!QAZxsw2"  # Webhook verify token (safe to hardcode for testing)


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
    """Test GET /status endpoint"""
    print_header("Testing GET /status endpoint")

    endpoint = f"{SERVER_URL}/status"
    print(f"URL: {endpoint}")

    try:
        # Make request
        response = requests.get(endpoint, timeout=TIMEOUT)

        # Check status code
        print_test(
            "HTTP Status Code",
            response.status_code == 200,
            f"Got {response.status_code}, expected 200"
        )

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

        print("\n📄 Full Response:")
        print(f"   {response.json()}")

        return True

    except requests.exceptions.Timeout:
        print_test("Request completed", False, f"Timeout after {TIMEOUT}s")
        return False
    except requests.exceptions.ConnectionError:
        print_test("Connection", False, "Could not connect to server")
        return False
    except Exception as e:
        print_test("Request completed", False, f"Error: {str(e)}")
        return False


def test_write_endpoint():
    """Test POST /write endpoint"""
    print_header("Testing POST /write endpoint")

    endpoint = f"{SERVER_URL}/write"
    print(f"URL: {endpoint}")

    # Test data
    test_texts = [
        "Hello, Render!",
        "Testing echo functionality",
        "こんにちは",  # Unicode test
        "12345",
        "Special chars: @#$%^&*()",
    ]

    all_passed = True

    for test_text in test_texts:
        print(f"\n🧪 Testing with: '{test_text}'")

        try:
            # Make request
            payload = {"text": test_text}
            response = requests.post(
                endpoint,
                json=payload,
                timeout=TIMEOUT
            )

            # Check status code
            status_ok = response.status_code == 200
            print_test(
                "HTTP Status Code",
                status_ok,
                f"Got {response.status_code}"
            )

            if not status_ok:
                all_passed = False
                continue

            # Parse JSON
            try:
                data = response.json()
                print_test("Response is valid JSON", True)
            except ValueError:
                print_test("Response is valid JSON", False)
                all_passed = False
                continue

            # Check echo matches
            echo_match = data.get('echo') == test_text
            print_test(
                "Echo matches input",
                echo_match,
                f"Got: '{data.get('echo')}'"
            )

            # Check length is correct
            length_correct = data.get('length') == len(test_text)
            print_test(
                "Length is correct",
                length_correct,
                f"Got: {data.get('length')}, Expected: {len(test_text)}"
            )

            # Check timestamp exists
            has_timestamp = 'timestamp' in data
            print_test(
                "Has timestamp",
                has_timestamp,
                data.get('timestamp', 'N/A')
            )

            if not (echo_match and length_correct and has_timestamp):
                all_passed = False

        except requests.exceptions.Timeout:
            print_test("Request completed", False, f"Timeout after {TIMEOUT}s")
            all_passed = False
        except requests.exceptions.ConnectionError:
            print_test("Connection", False, "Could not connect to server")
            all_passed = False
        except Exception as e:
            print_test("Request completed", False, f"Error: {str(e)}")
            all_passed = False

    return all_passed


def test_write_error_handling():
    """Test POST /write error handling"""
    print_header("Testing POST /write error handling")

    endpoint = f"{SERVER_URL}/write"
    print(f"URL: {endpoint}")

    # Test with missing 'text' field
    print("\n🧪 Testing with missing 'text' field")

    try:
        payload = {"message": "wrong field"}
        response = requests.post(
            endpoint,
            json=payload,
            timeout=TIMEOUT
        )

        # Should return 400 Bad Request
        is_400 = response.status_code == 400
        print_test(
            "Returns 400 for missing field",
            is_400,
            f"Got status code: {response.status_code}"
        )

        # Check error message
        if is_400:
            data = response.json()
            has_error = 'error' in data
            print_test(
                "Returns error message",
                has_error,
                f"Error: {data.get('error', 'N/A')}"
            )
            return has_error

        return is_400

    except Exception as e:
        print_test("Error handling test", False, f"Error: {str(e)}")
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


def main():
    """Run all tests"""
    print("\n")
    print("🧪 REMOTE SERVER HEALTH TEST")
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "Status Endpoint": test_status_endpoint(),
        "Write Endpoint": test_write_endpoint(),
        "Error Handling": test_write_error_handling(),
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
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
