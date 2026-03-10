"""
Git version utilities for deployment tracking
"""
import subprocess


def get_git_version():
    """
    Get current git commit information

    Returns:
        dict: Git version info with commit_id, commit_time, commit_message
    """
    try:
        # Get commit hash
        commit_id = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        # Get commit timestamp
        commit_time = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cI'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        # Get commit message
        commit_message = subprocess.check_output(
            ['git', 'log', '-1', '--format=%s'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        return {
            'commit_id': commit_id[:7],  # Short hash
            'commit_id_full': commit_id,
            'commit_time': commit_time,
            'commit_message': commit_message
        }
    except Exception as e:
        return {
            'commit_id': 'unknown',
            'commit_id_full': 'unknown',
            'commit_time': 'unknown',
            'commit_message': f'Error: {str(e)}'
        }
