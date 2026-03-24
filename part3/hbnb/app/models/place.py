#!/usr/bin/python3
"""
Place model module.
"""
from app.extensions import db
from app.models.base_model import BaseModel


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", backref="places", lazy=True)

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("places", lazy=True)
    )

    def __init__(self, title, description=None, price=0.0,
                 latitude=0.0, longitude=0.0, user_id=None):
        self._validate_and_set_title(title)
        self._validate_and_set_description(description)
        self._validate_and_set_price(price)
        self._validate_and_set_latitude(latitude)
        self._validate_and_set_longitude(longitude)
        self._validate_and_set_user_id(user_id)

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
        if not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        price = float(value)
        if price < 0:
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

    def _validate_and_set_user_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("user_id is required and must be a non-empty string")
        self.user_id = value.strip()

    def update(self, data):
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
        if "user_id" in data:
            self._validate_and_set_user_id(data["user_id"])

        self.save()