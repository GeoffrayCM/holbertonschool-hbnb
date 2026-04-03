import unittest
from app import create_app
from tests.utils import (
    reset_repositories, create_user, create_amenity, create_place
)


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        reset_repositories()
        self.app = create_app()
        self.client = self.app.test_client()

        # fixtures: one owner + two amenities
        user_resp = create_user(self.client, email="owner@example.com")
        self.assertEqual(user_resp.status_code, 201)
        self.owner_id = user_resp.get_json()["id"]

        a1 = create_amenity(self.client, name="Wi-Fi")
        a2 = create_amenity(self.client, name="Air Conditioning")
        self.assertEqual(a1.status_code, 201)
        self.assertEqual(a2.status_code, 201)
        self.amenity_ids = [a1.get_json()["id"], a2.get_json()["id"]]

    def test_create_place_ok(self):
        resp = create_place(self.client, self.owner_id, self.amenity_ids)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["owner_id"], self.owner_id)

    def test_create_place_invalid_latitude(self):
        resp = create_place(self.client, self.owner_id, self.amenity_ids, latitude=91.0)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_invalid_owner(self):
        resp = create_place(self.client, "does-not-exist", self.amenity_ids)
        self.assertEqual(resp.status_code, 400)

    def test_get_place_detail_includes_owner_and_amenities(self):
        place_resp = create_place(self.client, self.owner_id, self.amenity_ids)
        self.assertEqual(place_resp.status_code, 201)
        place_id = place_resp.get_json()["id"]

        resp = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("owner", data)
        self.assertIn("amenities", data)
        self.assertIsInstance(data["amenities"], list)


if __name__ == "__main__":
    unittest.main()