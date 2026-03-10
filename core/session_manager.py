"""
Session manager for message handling

Holds global state including the message handler registry.
"""
from core.message_handler import MessageHandler
from core.handler_callbacks.echo import echo_handler


class SessionManager:
    """
    Manages global message handling state

    This class holds the MessageHandler instance and registers
    default handler_callbacks. Should be initialized once on app startup.
    """

    def __init__(self):
        """Initialize session manager"""
        self.handler = MessageHandler()
        self._initialized = False

    def initialize(self) -> None:
        """
        Initialize the session manager

        Registers default handler_callbacks. Should be called once on app startup.
        """
        if self._initialized:
            print("Warning: SessionManager already initialized")
            return

        print("Initializing SessionManager...")

        # Register default handler_callbacks
        self.handler.register(echo_handler)

        self._initialized = True
        print("SessionManager initialized successfully")

    def process_message(self, message_data: dict) -> bool:
        """
        Process incoming message through registered handler_callbacks

        Args:
            message_data: Raw message data from Meta webhook

        Returns:
            bool: True if message was processed successfully, False otherwise
        """
        from core.message_metadata import MessageMetadata

        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")

        metadata = MessageMetadata.from_whatsapp_payload(message_data)
        return self.handler.process(metadata)
