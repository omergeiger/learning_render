"""
Message handler registry with callback support
"""
from typing import Callable, List
from core.message_metadata import MessageMetadata


# Type alias for handler callbacks
HandlerCallback = Callable[[MessageMetadata], bool]


class MessageHandler:
    """
    Message handler registry

    Allows registering multiple handler_callbacks that process incoming messages.
    Handlers are called in registration order until one succeeds.

    Example:
        handler = MessageHandler()

        def my_handler(metadata: MessageMetadata) -> bool:
            # Process message
            return True

        handler.register(my_handler)
        success = handler.process(metadata)
    """

    def __init__(self):
        """Initialize handler with empty callback list"""
        self._handlers: List[HandlerCallback] = []

    def register(self, handler: HandlerCallback) -> None:
        """
        Register a message handler callback

        Args:
            handler: Callable that takes MessageMetadata and returns bool
        """
        self._handlers.append(handler)
        print(f"Registered handler: {handler.__name__}")

    def process(self, metadata: MessageMetadata) -> bool:
        """
        Process message through registered handler_callbacks

        Handlers are called in registration order. Processing stops
        when a handler returns True (success) or all handler_callbacks are exhausted.

        Args:
            metadata: MessageMetadata instance to process

        Returns:
            bool: True if any handler succeeded, False otherwise
        """
        if not self._handlers:
            print("Warning: No handler_callbacks registered")
            return False

        print(f"Processing message from {metadata.from_number} (type: {metadata.message_type})")

        for handler in self._handlers:
            try:
                success = handler(metadata)
                if success:
                    print(f"Handler {handler.__name__} succeeded")
                    return True
                else:
                    print(f"Handler {handler.__name__} declined or failed")
            except Exception as e:
                print(f"Handler {handler.__name__} raised exception: {e}")
                continue

        print("No handler successfully processed the message")
        return False
