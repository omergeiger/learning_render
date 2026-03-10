"""
Main Flask application entry point
"""
from flask import Flask
from routes.status import status_bp
from routes.webhook import webhook_bp
from config import PORT, HOST
from core import SessionManager

# Create Flask app
app = Flask(__name__)

# Initialize session manager (holds global message handler state)
session_manager = SessionManager()


@app.before_request
def initialize_session():
    """Initialize session manager before first request"""
    if not session_manager._initialized:
        session_manager.initialize()


# Store session_manager in app context for routes to access
app.session_manager = session_manager

# Register blueprints
app.register_blueprint(status_bp)
app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
