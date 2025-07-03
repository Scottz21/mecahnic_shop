import unittest
from app import create_app
from app.models import db, Mechanic, ServiceTicket, Customer, service_mechanics
from datetime import date

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            mechanic = Mechanic(
                name="Jane Doe",
                email="jane@example.com",
                phone="555-123-4567",
                salary=50000.00
            )

            customer = Customer(
                name="Customer One",
                email="cust1@example.com",
                phone="555-000-0000",
                password="pass123"
            )

            db.session.add_all([mechanic, customer])
            db.session.commit()

            # Save IDs only to avoid DetachedInstanceError
            self.mechanic_id = mechanic.id
            self.customer_id = customer.id

    def test_create_mechanic(self):
        payload = {
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "555-987-6543",
            "salary": 60000.00
        }
        response = self.client.post("/mechanics/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Smith")

    def test_get_mechanics_no_pagination(self):
        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_mechanics_with_pagination(self):
        response = self.client.get("/mechanics/?page=1&per_page=1")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.json), 1)

    def test_update_mechanic(self):
        payload = {
            "phone": "999-888-7777",
            "salary": 65000.00
        }
        response = self.client.put(f"/mechanics/{self.mechanic_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["phone"], "999-888-7777")
        self.assertEqual(response.json["salary"], 65000.00)

    def test_delete_mechanic(self):
        response = self.client.delete(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(response.status_code, 204)

    def test_most_active_mechanics(self):
        with self.app.app_context():
            ticket = ServiceTicket(
                VIN="1HGCM82633A004352",
                service_date=date.today(),
                service_desc="Oil change and inspection",
                customer_id=self.customer_id
            )
            db.session.add(ticket)
            db.session.commit()

            stmt = service_mechanics.insert().values(
                ticket_id=ticket.id,
                mechanic_id=self.mechanic_id
            )
            db.session.execute(stmt)
            db.session.commit()

        response = self.client.get("/mechanics/most-active")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["id"], self.mechanic_id)
