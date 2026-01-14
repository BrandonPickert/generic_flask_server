"""WSGI entry point for the application."""
from app import create_app

# Create the Flask application instance
# For WSGI servers like Gunicorn: gunicorn wsgi:app
app = create_app()

if __name__ == '__main__':
    # This is used when running locally only
    # When deploying to production, use a proper WSGI server (gunicorn, uWSGI, etc.)
    import os
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
