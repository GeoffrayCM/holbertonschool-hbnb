#!/usr/bin/python3
"""
Review model module.
"""
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review entity."""

    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = None
        self.rating = None
        self.place = None
        self.user = None

        self._validate_and_set_text(text)
        self._validate_and_set_rating(rating)
        self._validate_and_set_place(place)
        self._validate_and_set_user(user)

    def _validate_and_set_text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required and must be a non-empty string")
        self.text = value.strip()

    def _validate_and_set_rating(self, value):
        if not isinstance(value, int):
            raise ValueError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        self.rating = value

    def _validate_and_set_place(self, value):
        if value is None:
            raise ValueError("place is required")
        if not isinstance(value, Place):
            raise ValueError("place must be a Place instance")
        self.place = value

    def _validate_and_set_user(self, value):
        if value is None:
            raise ValueError("user is required")
        if not isinstance(value, User):
            raise ValueError("user must be a User instance")
        self.user = value

    def update(self, data):
        """
        Update review fields with validation.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "text" in data:
            self._validate_and_set_text(data["text"])
        if "rating" in data:
            self._validate_and_set_rating(data["rating"])
        if "place" in data:
            self._validate_and_set_place(data["place"])
        if "user" in data:
            self._validate_and_set_user(data["user"])

        self.save()
