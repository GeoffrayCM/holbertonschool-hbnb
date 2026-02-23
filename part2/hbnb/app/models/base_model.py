#!/usr/bin/python3
"""
BaseModel module: shared attributes and basic update/save behavior.
"""
import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update existing attributes based on a dictionary.
        Protected fields cannot be updated.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        protected = {"id", "created_at", "updated_at"}
        for key, value in data.items():
            if key in protected:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()
