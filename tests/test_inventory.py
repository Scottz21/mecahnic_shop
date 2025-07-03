# tests/test_inventory.py
import unittest
from app import create_app
from app.models import db, Inventory

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            part = Inventory(name="Brake Pad", price=49.99)
            db.session.add(part)
            db.session.commit()

            self.part_id = part.id

    def test_create_part(self):
        payload = {
            "name": "Air Filter",
            "price": 19.99
        }
        response = self.client.post("/inventory/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["part"]["name"], "Air Filter")

    def test_get_parts(self):
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("parts", response.json)
        self.assertGreaterEqual(len(response.json["parts"]), 1)

    def test_update_part(self):
        payload = {
            "price": 59.99
        }
        response = self.client.put(f"/inventory/{self.part_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["part"]["price"], 59.99)

    def test_delete_part(self):
        response = self.client.delete(f"/inventory/{self.part_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Part deleted successfully")
