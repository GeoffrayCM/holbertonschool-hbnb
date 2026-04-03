#!/usr/bin/python3
"""
Amenity model module.
"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity."""

    def __init__(self, name):
        super().__init__()
        self.name = None
        self._validate_and_set_name(name)

    def _validate_and_set_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name is required and must be a non-empty string")
        name = value.strip()
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")
        self.name = name

    def update(self, data):
        """
        Update amenity fields with validation.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "name" in data:
            self._validate_and_set_name(data["name"])

        self.save()
