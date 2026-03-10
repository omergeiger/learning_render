"""
WhatsApp webhook endpoints
"""
from flask import Blueprint, request, jsonify, current_app
import traceback
from config import META_WA_VERIFY_TOKEN

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    WhatsApp webhook verification endpoint

    Use Case:
        - Called by Meta to verify webhook URL ownership during initial setup
        - Validates META_WA_VERIFY_TOKEN matches the token provided in Meta Developer Console
        - Returns challenge value to confirm webhook URL is valid
        - Called once during setup (or when webhook URL changes)

    Authentication: Verify token validation

    Query Parameters:
        - hub.mode: Should be 'subscribe'
        - hub.verify_token: Must match META_WA_VERIFY_TOKEN
        - hub.challenge: Value to return if verification succeeds

    Called by: Meta Developer Console when clicking "Verify and Save"
    """
    # Get parameters from the request

    print("!!! WEBHOOK GET FUNCTION CALLED !!! webhook_verify()")

    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    # Log the verification attempt
    print(f"Webhook verification attempt:")
    print(f"  mode={mode}")
    print(f"  received_token={token}")
    print(f"  expected_token={META_WA_VERIFY_TOKEN}")
    print(f"  token_match={token == META_WA_VERIFY_TOKEN}")
    print(f"  challenge={challenge}")

    # Verify the token and mode
    if mode == 'subscribe' and token == META_WA_VERIFY_TOKEN:
        # Respond with the challenge to verify
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        # Verification failed
        print("Webhook verification failed!")
        return 'Forbidden', 403


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_message():
    """
    WhatsApp incoming message handler

    Use Case:
        - Receives incoming WhatsApp messages from users
        - Parses Meta's webhook payload format
        - Implements echo logic: responds with "Echo: {message}"
        - Always returns 200 to acknowledge receipt (prevents Meta from retrying)

    Authentication: None (Meta sends to our verified webhook URL)

    Request Format:
        Meta's webhook format with nested entry/changes/messages structure

    Response:
        Always returns 200 OK with JSON status

    Called by: Meta's WhatsApp servers when users send messages to business number

    Current Logic:
        - Extract text messages only
        - Echo message back to sender with "Echo: " prefix
        - Ignore non-text messages
    """
    print("!!! WEBHOOK POST FUNCTION CALLED !!! webhook_message()")
    try:
        data = request.json

        # Extract message data from Meta's webhook format
        if 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value', {})

                    # Check if this is a message
                    messages = value.get('messages', [])
                    for message in messages:
                        # Process each message using session manager
                        current_app.session_manager.process_message(message)

        # Always return 200 to acknowledge receipt
        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        print("!!! EXCEPTION IN WEBHOOK !!!")
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        # Still return 200 to prevent Meta from retrying
        return jsonify({'status': 'error', 'message': str(e)}), 200
