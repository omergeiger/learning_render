"""
Business logic for processing WhatsApp messages
"""
from services.whatsapp import send_whatsapp_message


def process_message(message_data):
    """
    Process incoming WhatsApp message and determine response

    Args:
        message_data: Parsed message data from Meta webhook

    Returns:
        bool: True if message was processed successfully, False otherwise
    """
    from_number = message_data.get('from')
    message_type = message_data.get('type')

    # Only handle text messages
    if message_type == 'text':
        text_body = message_data.get('text', {}).get('body', '')

        print(f"Received message from {from_number}: {text_body}")

        # Echo the message back (current simple logic)
        echo_text = f"Echo: {text_body}"

        # Send response via WhatsApp (freetext)
        result = send_whatsapp_message(from_number, message_text=echo_text)

        if result:
            print(f"Echo sent successfully to {from_number}")
            return True
        else:
            print(f"Failed to send echo to {from_number}")
            return False

    return False
