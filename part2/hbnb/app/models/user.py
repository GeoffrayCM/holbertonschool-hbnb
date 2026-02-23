#!/usr/bin/python3
"""
User model module.
"""
import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User entity."""

    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = None
        self.last_name = None
        self.email = None
        self.is_admin = False

        self._validate_and_set_first_name(first_name)
        self._validate_and_set_last_name(last_name)
        self._validate_and_set_email(email)
        self._validate_and_set_is_admin(is_admin)

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
