"""Health check routes."""
from flask import Blueprint

health_bp = Blueprint('health', __name__)


@health_bp.route('/health')
def health_check():
    """Simple health check endpoint."""
    return {'status': 'healthy', 'service': 'generic-flask-server'}, 200


@health_bp.route('/')
def index():
    """Root endpoint."""
    return {
        'message': 'Generic Flask Server',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api'
        }
    }, 200
