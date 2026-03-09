"""
Application configuration and environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
META_WA_PHONE_ID = os.getenv('META_WA_PHONE_ID')
META_WA_ACCESS_TOKEN = os.getenv('META_WA_ACCESS_TOKEN')
META_WA_VERIFY_TOKEN = os.getenv('META_WA_VERIFY_TOKEN')

# WhatsApp Template Names
TEMPLATE_HELLO_WORLD = "hello_world"

# Server Configuration
PORT = int(os.getenv('PORT', 5000))
HOST = '0.0.0.0'
