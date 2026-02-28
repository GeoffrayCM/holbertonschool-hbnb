import unittest
from app import create_app
from tests.utils import reset_repositories


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        reset_repositories()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_ok(self):
        resp = self.client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Wi-Fi")

    def test_create_amenity_invalid_name(self):
        resp = self.client.post("/api/v1/amenities/", json={"name": ""})
        self.assertEqual(resp.status_code, 400)

    def test_get_amenities_list_ok(self):
        self.client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
        self.client.post("/api/v1/amenities/", json={"name": "Parking"})
        resp = self.client.get("/api/v1/amenities/")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_get_amenity_not_found(self):
        resp = self.client.get("/api/v1/amenities/does-not-exist")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()