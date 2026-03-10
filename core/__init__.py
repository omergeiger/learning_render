"""
Core message handling framework

Public API:
    - MessageMetadata: Structured message data
    - MessageHandler: Handler registry
    - SessionManager: Global state manager
"""
from core.message_metadata import MessageMetadata
from core.message_handler import MessageHandler
from core.session_manager import SessionManager

# Export public API
__all__ = ['MessageMetadata', 'MessageHandler', 'SessionManager']
