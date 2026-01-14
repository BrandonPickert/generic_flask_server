"""Flask application factory."""
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask

from app.config import config_by_name
from app.extensions import db, migrate, cors


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Configuration environment name (development, production, testing)
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Initialize extensions
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.api import api_bp
    from app.api.health import health_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Configure logging
    configure_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    app.logger.info(f'Flask app created with {config_name} configuration')
    
    return app


def configure_logging(app: Flask) -> None:
    """Configure application logging."""
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for the application."""
    from werkzeug.exceptions import HTTPException
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions."""
        return {
            'error': e.name,
            'message': e.description,
            'status': e.code
        }, e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle uncaught exceptions."""
        app.logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
        return {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status': 500
        }, 500
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return {
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }, 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handle 405 errors."""
        return {
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL',
            'status': 405
        }, 405
