import unittest
from app import create_app
from tests.utils import (
    reset_repositories, create_user, create_amenity, create_place, create_review
)


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        reset_repositories()
        self.app = create_app()
        self.client = self.app.test_client()

        # fixtures: user + amenity + place
        user_resp = create_user(self.client, email="reviewer@example.com")
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json()["id"]

        amenity_resp = create_amenity(self.client, name="Wi-Fi")
        self.assertEqual(amenity_resp.status_code, 201)
        amenity_id = amenity_resp.get_json()["id"]

        place_resp = create_place(self.client, self.user_id, [amenity_id])
        self.assertEqual(place_resp.status_code, 201)
        self.place_id = place_resp.get_json()["id"]

    def test_create_review_ok(self):
        resp = create_review(self.client, self.user_id, self.place_id, rating=5)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["user_id"], self.user_id)
        self.assertEqual(data["place_id"], self.place_id)

    def test_create_review_invalid_rating(self):
        resp = create_review(self.client, self.user_id, self.place_id, rating=6)
        self.assertEqual(resp.status_code, 400)

    def test_get_reviews_by_place_endpoint(self):
        r = create_review(self.client, self.user_id, self.place_id, text="Nice", rating=4)
        self.assertEqual(r.status_code, 201)

        resp = self.client.get(f"/api/v1/places/{self.place_id}/reviews")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_delete_review_removes_from_place_reviews(self):
        r = create_review(self.client, self.user_id, self.place_id, text="To delete", rating=4)
        self.assertEqual(r.status_code, 201)
        review_id = r.get_json()["id"]

        del_resp = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(del_resp.status_code, 200)

        # Verify not present anymore in nested list
        resp = self.client.get(f"/api/v1/places/{self.place_id}/reviews")
        self.assertEqual(resp.status_code, 200)
        reviews = resp.get_json()
        self.assertTrue(all(rv["id"] != review_id for rv in reviews))


if __name__ == "__main__":
    unittest.main()