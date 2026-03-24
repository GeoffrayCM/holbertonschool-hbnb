#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000/api/v1"

ADMIN_EMAIL = "admin@hbnb.io"
ADMIN_PASSWORD = "admin1234"

USER1 = {
    "first_name": "Alice",
    "last_name": "Owner",
    "email": "alice_rel_test@example.com",
    "password": "alice1234"
}

USER2 = {
    "first_name": "Bob",
    "last_name": "Reviewer",
    "email": "bob_rel_test@example.com",
    "password": "bob1234"
}


def pretty(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)


def request(method, path, data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return e.code, parsed
    except urllib.error.URLError as e:
        print("Impossible de contacter l'API.")
        print("Vérifiez que python3 run.py tourne bien sur http://127.0.0.1:5000")
        print(f"Détail: {e}")
        sys.exit(1)


def assert_status(actual, expected, context, payload=None):
    if actual != expected:
        print(f"\n❌ {context}")
        print(f"Statut reçu: {actual}, attendu: {expected}")
        if payload is not None:
            print(pretty(payload))
        sys.exit(1)


def assert_true(condition, context, payload=None):
    if not condition:
        print(f"\n❌ {context}")
        if payload is not None:
            print(pretty(payload))
        sys.exit(1)


def print_step(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def login(email, password):
    status, payload = request("POST", "/auth/login", {
        "email": email,
        "password": password
    })
    assert_status(status, 200, f"Login échoué pour {email}", payload)
    token = payload.get("access_token")
    assert_true(bool(token), f"Token absent pour {email}", payload)
    return token


def create_user_as_admin(admin_token, user_data):
    status, payload = request("POST", "/users/", user_data, admin_token)

    # 201 = créé
    # 400 = existe déjà / email déjà pris
    assert_true(status in (201, 400), f"Création user inattendue {user_data['email']}", payload)

    if status == 201:
        return payload.get("id")

    # si déjà créé, on le retrouve dans la liste
    status, users = request("GET", "/users/")
    assert_status(status, 200, "Impossible de récupérer la liste des users", users)

    for user in users:
        if user.get("email") == user_data["email"]:
            return user.get("id")

    print(f"\n❌ User {user_data['email']} introuvable après réponse 400")
    print(pretty(payload))
    sys.exit(1)


def create_amenity_as_admin(admin_token, name):
    status, payload = request("POST", "/amenities/", {"name": name}, admin_token)

    # 201 = créé
    # 400 = peut déjà exister selon vos validations
    assert_true(status in (201, 400), f"Création amenity inattendue {name}", payload)

    if status == 201:
        return payload.get("id")

    status, amenities = request("GET", "/amenities/")
    assert_status(status, 200, "Impossible de récupérer la liste des amenities", amenities)

    for amenity in amenities:
        if amenity.get("name") == name:
            return amenity.get("id")

    print(f"\n❌ Amenity {name} introuvable après réponse 400")
    print(pretty(payload))
    sys.exit(1)


def main():
    print_step("1) Login admin")
    admin_token = login(ADMIN_EMAIL, ADMIN_PASSWORD)
    print("✅ Admin connecté")

    print_step("2) Création / récupération de 2 users normaux")
    user1_id = create_user_as_admin(admin_token, USER1)
    user2_id = create_user_as_admin(admin_token, USER2)
    print(f"✅ User1 id: {user1_id}")
    print(f"✅ User2 id: {user2_id}")

    print_step("3) Login user1 et user2")
    user1_token = login(USER1["email"], USER1["password"])
    user2_token = login(USER2["email"], USER2["password"])
    print("✅ User1 connecté")
    print("✅ User2 connecté")

    print_step("4) Création / récupération de 2 amenities")
    wifi_id = create_amenity_as_admin(admin_token, "WiFi")
    pool_id = create_amenity_as_admin(admin_token, "Pool")
    print(f"✅ WiFi id: {wifi_id}")
    print(f"✅ Pool id: {pool_id}")

    print_step("5) Création d'une place par user1 avec 2 amenities")
    place_payload = {
        "title": "Maison relation test",
        "description": "Validation relations SQLAlchemy",
        "price": 120,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "ignored-by-api",
        "amenities": [wifi_id, pool_id],
        "reviews": []
    }
    status, place_resp = request("POST", "/places/", place_payload, user1_token)
    assert_status(status, 201, "Création de place échouée", place_resp)
    place_id = place_resp.get("id")
    assert_true(bool(place_id), "ID de place absent", place_resp)
    print(f"✅ Place créée: {place_id}")

    print_step("6) Lecture de la place et vérification owner + amenities")
    status, place_detail = request("GET", f"/places/{place_id}")
    assert_status(status, 200, "Lecture de place échouée", place_detail)

    assert_true(place_detail.get("owner_id") == user1_id,
                "owner_id incorrect sur la place", place_detail)

    owner = place_detail.get("owner", {})
    assert_true(owner.get("id") == user1_id,
                "Relation place.owner incorrecte", place_detail)

    amenities = place_detail.get("amenities", [])
    amenity_ids = {a.get("id") for a in amenities}
    assert_true(len(amenities) == 2,
                "La place devrait avoir 2 amenities", place_detail)
    assert_true({wifi_id, pool_id}.issubset(amenity_ids),
                "Les amenities liées à la place ne sont pas correctes", place_detail)

    print("✅ Relation User <-> Place OK")
    print("✅ Relation Place <-> Amenity OK")

    print_step("7) Création d'un review par user2")
    review_payload = {
        "text": "Très bon logement",
        "rating": 5,
        "place_id": place_id
    }
    status, review_resp = request("POST", "/reviews/", review_payload, user2_token)
    assert_status(status, 201, "Création de review échouée", review_resp)
    review_id = review_resp.get("id")
    assert_true(bool(review_id), "ID de review absent", review_resp)
    print(f"✅ Review créé: {review_id}")

    print_step("8) Vérification review.user et review.place")
    status, review_detail = request("GET", f"/reviews/{review_id}")
    assert_status(status, 200, "Lecture du review échouée", review_detail)

    assert_true(review_detail.get("user_id") == user2_id,
                "Relation Review -> User incorrecte", review_detail)
    assert_true(review_detail.get("place_id") == place_id,
                "Relation Review -> Place incorrecte", review_detail)

    print("✅ Relation User <-> Review OK")
    print("✅ Relation Place <-> Review OK")

    print_step("9) Relire la place et vérifier que le review remonte")
    status, place_detail_2 = request("GET", f"/places/{place_id}")
    assert_status(status, 200, "Lecture détaillée de place échouée après review", place_detail_2)

    reviews = place_detail_2.get("reviews", [])
    assert_true(len(reviews) == 1,
                "La place devrait remonter exactement 1 review", place_detail_2)

    first_review = reviews[0]
    assert_true(first_review.get("id") == review_id,
                "Le review remonté dans la place n'est pas le bon", place_detail_2)
    assert_true(first_review.get("user_id") == user2_id,
                "Le review remonté dans la place n'a pas le bon user_id", place_detail_2)

    print("✅ place.reviews OK")

    print_step("10) Endpoint /places/<place_id>/reviews")
    status, place_reviews = request("GET", f"/places/{place_id}/reviews")
    assert_status(status, 200, "Liste des reviews par place échouée", place_reviews)
    assert_true(isinstance(place_reviews, list) and len(place_reviews) == 1,
                "La liste des reviews de la place devrait contenir 1 élément", place_reviews)
    assert_true(place_reviews[0].get("id") == review_id,
                "Le review listé pour la place n'est pas le bon", place_reviews)

    print("✅ Endpoint place -> reviews OK")

    print_step("11) Test négatif : owner ne peut pas reviewer sa propre place")
    status, payload = request("POST", "/reviews/", {
        "text": "Je review mon propre logement",
        "rating": 5,
        "place_id": place_id
    }, user1_token)
    assert_status(status, 400, "Le owner ne devrait pas pouvoir reviewer sa propre place", payload)
    print("✅ Règle 'pas son propre logement' OK")

    print_step("12) Test négatif : même user ne peut pas reviewer 2 fois la même place")
    status, payload = request("POST", "/reviews/", {
        "text": "Deuxième review interdit",
        "rating": 4,
        "place_id": place_id
    }, user2_token)
    assert_status(status, 400, "Le même user ne devrait pas pouvoir reviewer 2 fois", payload)
    print("✅ Règle 'un seul review par user/place' OK")

    print_step("13) Résultat final")
    print("✅ Toutes les vérifications principales sont passées")
    print("Relations validées :")
    print("   - User <-> Place")
    print("   - Place <-> Amenity")
    print("   - Place <-> Review")
    print("   - User <-> Review")


if __name__ == "__main__":
    main()