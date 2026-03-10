"""
Health check and status endpoints
"""
from flask import Blueprint, jsonify
from datetime import datetime, UTC
from utils.version import get_git_version

status_bp = Blueprint('status', __name__)


@status_bp.route('/status', methods=['GET'])
def status():
    """
    Health check and deployment verification endpoint

    Use Case:
        - Monitoring: Verify server is running
        - Deployment verification: Check which git commit is deployed
        - Called by: Monitoring tools, manual checks, test scripts

    Authentication: None required

    Returns:
        JSON with status, timestamp, and git version info (commit_id, commit_time, commit_message)

    Example:
        curl https://learning-render-ut2u.onrender.com/status
    """
    print("!!! STATUS GET FUNCTION CALLED !!! status()")

    version_info = get_git_version()
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now(UTC).isoformat(),
        'message': 'Server is running',
        'version': version_info
    })
