from flask import Flask, request, jsonify
import os
from datetime import datetime, UTC

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now(UTC).isoformat(),
        'message': 'Server is running'
    })

@app.route('/write', methods=['POST'])
def write():
    """Echo endpoint - returns input text"""
    data = request.json

    if not data or 'text' not in data:
        return jsonify({
            'error': 'Missing text field in request body'
        }), 400

    input_text = data['text']

    return jsonify({
        'echo': input_text,
        'length': len(input_text),
        'timestamp': datetime.now(UTC).isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
