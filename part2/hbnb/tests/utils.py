# tests/utils.py
# Small helpers shared by tests (reset in-memory repos + create fixtures)
# python3 -m unittest discover -s tests -p "test_*.py" -v
from app.services import facade


def reset_repositories():
    """
    Because the facade is a singleton and repos are in-memory,
    tests can leak state across test cases.
    We hard-reset the internal storage dicts.
    """
    for repo_name in ("user_repo", "amenity_repo", "place_repo", "review_repo"):
        repo = getattr(facade, repo_name, None)
        if repo and hasattr(repo, "_storage"):
            repo._storage.clear()


def create_user(client, first_name="John", last_name="Doe", email="john@example.com"):
    resp = client.post("/api/v1/users/", json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    })
    return resp


def create_amenity(client, name="Wi-Fi"):
    resp = client.post("/api/v1/amenities/", json={"name": name})
    return resp


def create_place(client, owner_id, amenity_ids, title="Cozy Apartment",
                 price=100.0, latitude=37.7749, longitude=-122.4194, description="Nice"):
    resp = client.post("/api/v1/places/", json={
        "title": title,
        "description": description,
        "price": price,
        "latitude": latitude,
        "longitude": longitude,
        "owner_id": owner_id,
        "amenities": amenity_ids
    })
    return resp


def create_review(client, user_id, place_id, text="Great stay!", rating=5):
    resp = client.post("/api/v1/reviews/", json={
        "text": text,
        "rating": rating,
        "user_id": user_id,
        "place_id": place_id
    })
    return resp