#!/usr/bin/python3
"""
User model module.
"""
import re
from app.extensions import db
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        self._validate_and_set_first_name(first_name)
        self._validate_and_set_last_name(last_name)
        self._validate_and_set_email(email)
        self._validate_and_set_is_admin(is_admin)

        if password is not None:
            self.hash_password(password)

    def _validate_and_set_first_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("first_name is required and must be a non-empty string")
        if len(value) > 50:
            raise ValueError("first_name must be at most 50 characters")
        self.first_name = value.strip()

    def _validate_and_set_last_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("last_name is required and must be a non-empty string")
        if len(value) > 50:
            raise ValueError("last_name must be at most 50 characters")
        self.last_name = value.strip()

    def _validate_and_set_email(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required and must be a non-empty string")
        email = value.strip()
        if not self.EMAIL_REGEX.match(email):
            raise ValueError("email format is invalid")
        self.email = email

    def _validate_and_set_is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self.is_admin = value

    # Receive clear password (ex: user.hash_p("my password"))
    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app.extensions import bcrypt # bcrypt available only after app is fully initialized
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Compare password used with password saved, directly comparing hashed version
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app.extensions import bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        """
        Update user fields with validation.
        Only updates known fields and keeps BaseModel behavior.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "first_name" in data:
            self._validate_and_set_first_name(data["first_name"])
        if "last_name" in data:
            self._validate_and_set_last_name(data["last_name"])
        if "email" in data:
            self._validate_and_set_email(data["email"])
        if "is_admin" in data:
            self._validate_and_set_is_admin(data["is_admin"])

        self.save()
