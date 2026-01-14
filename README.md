# Generic Flask Server

A production-ready, modular Flask WSGI server template following modern best practices and conventions.

## Features

- **Application Factory Pattern**: Clean, modular application structure
- **Blueprint-based Architecture**: Organized API routes and endpoints
- **Environment-based Configuration**: Separate configs for development, production, and testing
- **CORS Support**: Built-in Cross-Origin Resource Sharing configuration
- **Error Handling**: Comprehensive error handlers for common HTTP errors
- **Logging**: Rotating file logs with configurable levels
- **Health Check Endpoint**: Monitor application status
- **Testing Suite**: pytest-based tests with coverage reporting
- **WSGI Production Ready**: Configured for Gunicorn deployment

## Project Structure

```
generic_flask_server/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration classes
│   ├── extensions.py        # Flask extensions (db, migrate, cors)
│   ├── api/                 # API blueprints
│   │   ├── __init__.py      # API blueprint registration
│   │   ├── routes.py        # API endpoints
│   │   └── health.py        # Health check routes
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py      # Models package
│   │   └── models.py        # Database models (User example commented)
│   ├── services/            # Business logic layer
│   │   └── __init__.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py       # Helper functions
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       └── index.html
├── tests/                   # Test suite
│   ├── conftest.py
│   └── test_api.py
├── instance/                # Instance-specific files (not in git)
├── logs/                    # Application logs (created at runtime)
├── wsgi.py                  # WSGI entry point
├── manage.py                # CLI management script
├── gunicorn_config.py       # Gunicorn configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Project configuration
├── .env.example             # Environment variables template
├── Procfile                 # Heroku deployment
├── .gitignore
├── run_dev.sh              # Development server script
└── run_prod.sh             # Production server script
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd generic_flask_server
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The application supports three environments:

- **Development**: Debug mode enabled, SQLite database, verbose logging
- **Production**: Optimized for deployment, secure settings, PostgreSQL ready
- **Testing**: In-memory database, testing-specific settings

Configure via the `FLASK_ENV` environment variable or in your `.env` file.

## Running the Application

### Using Management CLI

```bash
# Run development server
python manage.py run

# Initialize database
python manage.py init-db

# Drop database tables
python manage.py drop-db

# Run Flask migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Development Server

```bash
# Using the script
chmod +x run_dev.sh
./run_dev.sh

# Or directly with Python
python wsgi.py

# Or with Flask CLI
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

The development server will start on `http://localhost:5000`

### Production Server (Gunicorn)

```bash
# Using the script
chmod +x run_prod.sh
./run_prod.sh

# Or directly
gunicorn --config gunicorn_config.py wsgi:app
```

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### API Endpoints

- `GET /api/` - API index
- `GET /api/examples` - Get all examples
- `GET /api/examples/<id>` - Get specific example
- `POST /api/examples` - Create new example
- `PUT /api/examples/<id>` - Update example
- `DELETE /api/examples/<id>` - Delete example
- `POST /api/echo` - Echo endpoint for testing

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## Environment Variables

Key environment variables (see `.env.example` for complete list):

- `FLASK_ENV`: Application environment (development/production/testing)
- `SECRET_KEY`: Secret key for sessions and security
- `HOST`: Server host address (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

## Deployment

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run flask db upgrade
```

### Other Cloud Platforms

This application is ready to deploy to:
- **AWS Elastic Beanstalk**: Use the included `wsgi.py`
- **Azure App Service**: Configure startup command to use Gunicorn
- **PythonAnywhere**: Upload files and configure WSGI
- **DigitalOcean App Platform**: Use `gunicorn wsgi:app` as run command

## Development

### Adding New Endpoints

1. Create route functions in `app/api/routes.py`
2. Use blueprints for organization
3. Add corresponding tests in `tests/test_api.py`

### Adding Models

1. Create model classes in `app/models/`
2. Implement serialization methods (`to_dict`, `from_dict`)

### Adding Services

1. Create service classes in `app/services/`
2. Implement business logic separate from routes

## Security Best Practices

- ✅ Environment-based configuration
- ✅ Secret key management via environment variables
- ✅ CORS protection
- ✅ Request size limits
- ✅ Secure session cookies in production
- ✅ Comprehensive error handling without exposing internals
- ✅ Input validation helpers

## License

MIT License - feel free to use this template for your projects.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please open an issue in the repository.
