"""
Echo handler - responds with "Echo: {message}"
"""
from core.message_metadata import MessageMetadata
from utils.whatsapp import send_whatsapp_message


def echo_handler(metadata: MessageMetadata) -> bool:
    """
    Echo handler - responds with "Echo: {message}"

    Args:
        metadata: Message metadata

    Returns:
        bool: True if echo was sent successfully, False otherwise
    """
    if not metadata.is_text_message():
        return False

    print(f"Echo handler: Received message from {metadata.from_number}: {metadata.text_body}")

    # Echo the message back
    echo_text = f"Echo: {metadata.text_body}"

    # Send response via WhatsApp
    result = send_whatsapp_message(metadata.from_number, message_text=echo_text)

    if result:
        print(f"Echo sent successfully to {metadata.from_number}")
        return True
    else:
        print(f"Failed to send echo to {metadata.from_number}")
        return False
