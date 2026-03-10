"""
Message metadata extraction from WhatsApp payloads
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageMetadata:
    """
    Structured metadata extracted from WhatsApp message payload

    Attributes:
        from_number: Sender's phone number (with country code, no +)
        message_type: Type of message (text, image, audio, etc.)
        text_body: Text content (for text messages)
        message_id: Unique message identifier from WhatsApp
        timestamp: Message timestamp from WhatsApp
    """
    from_number: str
    message_type: str
    text_body: Optional[str] = None
    message_id: Optional[str] = None
    timestamp: Optional[str] = None

    @classmethod
    def from_whatsapp_payload(cls, message_data: dict) -> 'MessageMetadata':
        """
        Extract metadata from Meta's WhatsApp webhook message format

        Args:
            message_data: Raw message dict from Meta's webhook payload

        Returns:
            MessageMetadata instance with extracted fields
        """
        from_number = message_data.get('from', '')
        message_type = message_data.get('type', '')
        message_id = message_data.get('id')
        timestamp = message_data.get('timestamp')

        # Extract text body for text messages
        text_body = None
        if message_type == 'text':
            text_body = message_data.get('text', {}).get('body', '')

        return cls(
            from_number=from_number,
            message_type=message_type,
            text_body=text_body,
            message_id=message_id,
            timestamp=timestamp
        )

    def is_text_message(self) -> bool:
        """Check if this is a text message"""
        return self.message_type == 'text' and self.text_body is not None
