#!/usr/bin/python3
"""
Review model module.
"""
from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    place = db.relationship("Place", backref="reviews", lazy=True)
    user = db.relationship("User", backref="reviews", lazy=True)

    def __init__(self, text, rating, place_id, user_id):
        self._validate_and_set_text(text)
        self._validate_and_set_rating(rating)
        self._validate_and_set_place_id(place_id)
        self._validate_and_set_user_id(user_id)

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

    def _validate_and_set_place_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("place_id is required and must be a non-empty string")
        self.place_id = value.strip()

    def _validate_and_set_user_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("user_id is required and must be a non-empty string")
        self.user_id = value.strip()

    def update(self, data):
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if "text" in data:
            self._validate_and_set_text(data["text"])
        if "rating" in data:
            self._validate_and_set_rating(data["rating"])
        if "place_id" in data:
            self._validate_and_set_place_id(data["place_id"])
        if "user_id" in data:
            self._validate_and_set_user_id(data["user_id"])

        self.save()