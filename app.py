"""
Main Flask application entry point
"""
from flask import Flask
from routes.status import status_bp
from routes.webhook import webhook_bp
from config import PORT, HOST

# Create Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(status_bp)
app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
