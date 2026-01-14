#!/bin/bash

# Development server startup script
echo "Starting Flask development server..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set development environment
export FLASK_ENV=development
export FLASK_APP=wsgi.py

# Run the development server
python3 wsgi.py
