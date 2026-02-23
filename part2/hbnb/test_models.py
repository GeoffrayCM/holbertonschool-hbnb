#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user():
    user = User("John", "Doe", "john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User test passed!")


def test_place():
    owner = User("Alice", "Smith", "alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="Nice place",
        price=100,
        latitude=40.7128,
        longitude=-74.0060,
        owner=owner
    )

    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.owner == owner
    print("Place test passed!")


def test_review():
    owner = User("Bob", "Marley", "bob@example.com")
    place = Place(
        title="Beach House",
        description="Ocean view",
        price=200,
        latitude=25.7617,
        longitude=-80.1918,
        owner=owner
    )

    review = Review(
        text="Amazing stay!",
        rating=5,
        place=place,
        user=owner
    )

    place.add_review(review)

    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Amazing stay!"
    assert review.place == place
    print("Review test passed!")


def test_amenity():
    amenity = Amenity("Wi-Fi")
    owner = User("Emma", "Stone", "emma@example.com")

    place = Place(
        title="Modern Studio",
        description="City center",
        price=150,
        latitude=48.8566,
        longitude=2.3522,
        owner=owner
    )

    place.add_amenity(amenity)

    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wi-Fi"
    print("Amenity test passed!")


def test_updates():
    user = User("Old", "Name", "old@example.com")
    user.update({"first_name": "New", "is_admin": True})
    assert user.first_name == "New"
    assert user.is_admin is True

    amenity = Amenity("Parking")
    amenity.update({"name": "Free Parking"})
    assert amenity.name == "Free Parking"

    print("Update test passed!")


if __name__ == "__main__":
    test_user()
    test_place()
    test_review()
    test_amenity()
    test_updates()
    print("\nAll model tests passed successfully!")
