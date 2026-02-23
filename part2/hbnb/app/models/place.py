#!/usr/bin/python3
"""
Place model module.
"""
from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place entity."""

    def __init__(self, title, description=None, price=0.0,
                 latitude=0.0, longitude=0.0, owner=None):
        super().__init__()

        self.title = None
        self.description = None
        self.price = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.owner = None

        # Relationships
        self.reviews = []
        self.amenities = []

        self._validate_and_set_title(title)
        self._validate_and_set_description(description)
        self._validate_and_set_price(price)
        self._validate_and_set_latitude(latitude)
        self._validate_and_set_longitude(longitude)
        self._validate_and_set_owner(owner)

    def _validate_and_set_title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title is required and must be a non-empty string")
        title = value.strip()
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")
        self.title = title

    def _validate_and_set_description(self, value):
        if value is None:
            self.description = None
            return
        if not isinstance(value, str):
            raise ValueError("description must be a string or None")
        desc = value.strip()
        self.description = desc if desc else None

    def _validate_and_set_price(self, value):
        # Accept int or float, store as float
        if not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        price = float(value)
        if price <= 0:
            raise ValueError("price must be a positive value")
        self.price = price

    def _validate_and_set_latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        lat = float(value)
        if lat < -90.0 or lat > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        self.latitude = lat

    def _validate_and_set_longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        lon = float(value)
        if lon < -180.0 or lon > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        self.longitude = lon

    def _validate_and_set_owner(self, value):
        if value is None:
            raise ValueError("owner is required")
        if not isinstance(value, User):
            raise ValueError("owner must be a User instance")
        self.owner = value

    def add_review(self, review):
        """Add a review to the place."""
        # We only validate minimal structure here to avoid depending on Review class logic
        if review is None:
            raise ValueError("review cannot be None")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity is None:
            raise ValueError("amenity cannot be None")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def update(self, data):
        """
        Update place fields with validation.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "title" in data:
            self._validate_and_set_title(data["title"])
        if "description" in data:
            self._validate_and_set_description(data["description"])
        if "price" in data:
            self._validate_and_set_price(data["price"])
        if "latitude" in data:
            self._validate_and_set_latitude(data["latitude"])
        if "longitude" in data:
            self._validate_and_set_longitude(data["longitude"])
        if "owner" in data:
            self._validate_and_set_owner(data["owner"])

        self.save()
