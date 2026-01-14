#!/bin/bash

# Production server startup script
echo "Starting Flask production server with Gunicorn..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set production environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn --config gunicorn_config.py wsgi:app
