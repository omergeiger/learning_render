"""
WhatsApp Business API integration
"""
import requests
from config import (
    WHATSAPP_API_URL,
    META_WA_PHONE_ID,
    META_WA_ACCESS_TOKEN,
    TEMPLATE_HELLO_WORLD
)


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
