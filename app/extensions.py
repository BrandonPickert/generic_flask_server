"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions (will be bound to app in factory)
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
