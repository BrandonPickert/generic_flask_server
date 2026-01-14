from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


# Example User model (commented out - uncomment and modify as needed)
# class User(db.Model):
#     """User model."""
#     
#     __tablename__ = 'users'
#     
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False, index=True)
#     email = db.Column(db.String(120), unique=True, nullable=False, index=True)
#     password_hash = db.Column(db.String(255), nullable=False)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     is_active = db.Column(db.Boolean, default=True, nullable=False)
#     is_admin = db.Column(db.Boolean, default=False, nullable=False)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
#     updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
#     
#     def __repr__(self):
#         return f'<User {self.username}>'
#     
#     def set_password(self, password):
#         """Hash and set the user's password."""
#         self.password_hash = generate_password_hash(password)
#     
#     def check_password(self, password):
#         """Check if provided password matches the hash."""
#         return check_password_hash(self.password_hash, password)
#     
#     def to_dict(self):
#         """Convert user to dictionary (excluding password)."""
#         return {
#             'id': self.id,
#             'username': self.username,
#             'email': self.email,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'is_active': self.is_active,
#             'is_admin': self.is_admin,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None
#         }
