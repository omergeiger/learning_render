from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime, UTC
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)

# WhatsApp Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
META_WA_PHONE_ID = os.getenv('META_WA_PHONE_ID')
META_WA_ACCESS_TOKEN = os.getenv('META_WA_ACCESS_TOKEN')
META_WA_VERIFY_TOKEN = os.getenv('META_WA_VERIFY_TOKEN')

# WhatsApp Template Names
TEMPLATE_HELLO_WORLD = "hello_world"


def send_whatsapp_message(to_phone_number, message_text=None, template_name=None, template_language="en_US"):
    """
    Send a message via WhatsApp Business API (template or freetext)

    Args:
        to_phone_number: Recipient phone number (with country code, no +)
        message_text: Text message to send (for freetext messages)
        template_name: Template name to use (for template messages)
        template_language: Language code for template (default: "en_US")

    Returns:
        Response from WhatsApp API or None on error

    Examples:
        # Send freetext message
        send_whatsapp_message("1234567890", message_text="Hello!")

        # Send template message
        send_whatsapp_message("1234567890", template_name=TEMPLATE_HELLO_WORLD)
    """
    url = f"{WHATSAPP_API_URL}/{META_WA_PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {META_WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Determine message type and build payload
    if template_name:
        # Template message
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": template_language
                }
            }
        }
        print(f"Sending template message: {template_name} to {to_phone_number}")

    elif message_text:
        # Freetext message
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        print(f"Sending text message to {to_phone_number}: {message_text[:50]}...")

    else:
        print("Error: Must provide either message_text or template_name")
        return None

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"WhatsApp API response: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending WhatsApp message: {e}")
        if hasattr(e.response, 'text'):
            print(f"API error details: {e.response.text}")
        return None

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now(UTC).isoformat(),
        'message': 'Server is running'
    })

@app.route('/write', methods=['POST'])
def write():
    """Echo endpoint - returns input text"""
    data = request.json

    if not data or 'text' not in data:
        return jsonify({
            'error': 'Missing text field in request body'
        }), 400

    input_text = data['text']

    return jsonify({
        'echo': input_text,
        'length': len(input_text),
        'timestamp': datetime.now(UTC).isoformat()
    })


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    Webhook verification endpoint for WhatsApp
    Meta calls this to verify the webhook URL
    """
    # Get parameters from the request
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


@app.route('/webhook', methods=['POST'])
def webhook_message():
    """
    Webhook endpoint for receiving WhatsApp messages
    Meta sends incoming messages here
    """
    try:
        data = request.json
        print("=" * 50)
        print("WEBHOOK RECEIVED!")
        print(f"Received webhook: {data}")
        print("=" * 50)

        # Extract message data from Meta's webhook format
        if 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value', {})

                    # Check if this is a message
                    messages = value.get('messages', [])
                    for message in messages:
                        # Extract message details
                        from_number = message.get('from')
                        message_type = message.get('type')

                        # Only handle text messages
                        if message_type == 'text':
                            text_body = message.get('text', {}).get('body', '')

                            print(f"Received message from {from_number}: {text_body}")

                            # Echo the message back (our simple logic)
                            echo_text = f"Echo: {text_body}"

                            # Send response via WhatsApp (freetext)
                            result = send_whatsapp_message(from_number, message_text=echo_text)

                            if result:
                                print(f"Echo sent successfully to {from_number}")
                            else:
                                print(f"Failed to send echo to {from_number}")

        # Always return 200 to acknowledge receipt
        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        # Still return 200 to prevent Meta from retrying
        return jsonify({'status': 'error', 'message': str(e)}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
