import unittest
from app import create_app
from tests.utils import reset_repositories


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        reset_repositories()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_ok(self):
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "jane.doe@example.com")

    def test_create_user_invalid_email(self):
        resp = self.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_user_duplicate_email(self):
        resp1 = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "dup@example.com"
        })
        self.assertEqual(resp1.status_code, 201)

        resp2 = self.client.post("/api/v1/users/", json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "dup@example.com"
        })
        self.assertEqual(resp2.status_code, 400)

    def test_get_user_not_found(self):
        resp = self.client.get("/api/v1/users/does-not-exist")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()