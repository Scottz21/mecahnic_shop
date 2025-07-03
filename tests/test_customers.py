import unittest
from app import create_app
from app.models import db, Customer


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        self.customer = Customer(
            name="Test User",
            email="test@example.com",
            phone="123-456-7890",
            password="test"
        )

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()

    def login_customer(self):
        return self.client.post("/customers/login", json={
            "email": "test@example.com",
            "password": "test"
        }, follow_redirects=True)

    def test_create_customer(self):
        payload = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "111-222-3333",
            "password": "secure"
        }
        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Jane Smith")

    def test_create_customer_missing_email(self):
        payload = {
            "name": "Jeff Smith",
            "phone": "111-222-3333",
            "password": "secure"
        }
        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)

    def test_login_customer_success(self):
        response = self.login_customer()
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_customer_failure(self):
        credentials = {
            "email": "wrong@example.com",
            "password": "wrong"
        }
        response = self.client.post("/customers/login", json=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Invalid email or password!")

    def test_get_all_customers(self):
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_delete_customer_authenticated(self):
        login_response = self.login_customer()
        token = login_response.json.get("token")
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.delete("/customers/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Customer deleted successfully")

    def test_delete_customer_missing_token(self):
        response = self.client.delete("/customers/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Authorization header missing")
