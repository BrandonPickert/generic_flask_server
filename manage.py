"""Management CLI for the application."""
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db

def create_app_for_cli():
    """Create app instance for CLI."""
    return create_app()

cli = FlaskGroup(create_app=create_app_for_cli)


@cli.command("init-db")
def init_db():
    """Initialize the database."""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database initialized!")


@cli.command("drop-db")
def drop_db():
    """Drop all database tables."""
    if input("Are you sure you want to drop all tables? (yes/no): ").lower() == 'yes':
        app = create_app()
        with app.app_context():
            db.drop_all()
            print("Database tables dropped!")
    else:
        print("Operation cancelled.")


if __name__ == '__main__':
    cli()
