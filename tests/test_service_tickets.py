import unittest
from datetime import date
from app import create_app
from app.models import db, ServiceTicket, Customer, Mechanic, Inventory, TicketPart

class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            customer = Customer(
                name="Ticket Tester",
                email="ticket@example.com",
                phone="123-456-7890",
                password="secret"
            )

            mechanic = Mechanic(
                name="Mechanic One",
                email="mech1@example.com",
                phone="111-222-3333",
                salary=55000.0
            )

            part = Inventory(name="Oil Filter", price=29.99)

            db.session.add_all([customer, mechanic, part])
            db.session.commit()

            self.customer_id = customer.id
            self.mechanic_id = mechanic.id
            self.part_id = part.id

            ticket = ServiceTicket(
                VIN="TESTVIN123456",
                service_date=date.today(),
                service_desc="Initial inspection",
                customer_id=self.customer_id
            )
            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id

    def test_create_ticket(self):
        payload = {
            "VIN": "XYZ123456789",
            "service_date": str(date.today()),
            "service_desc": "Brake pad replacement",
            "customer_id": self.customer_id
        }
        response = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["VIN"], "XYZ123456789")

    def test_get_all_tickets(self):
        response = self.client.get("/service-tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_tickets_with_pagination(self):
        response = self.client.get("/service-tickets/?page=1&per_page=1")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.json), 1)

    def test_assign_mechanic_to_ticket(self):
        response = self.client.put(f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("mechanics", response.json)
        self.assertEqual(response.json["mechanics"][0]["id"], self.mechanic_id)

    def test_remove_mechanic_from_ticket(self):
        # First assign
        self.client.put(f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}")
        # Then remove
        response = self.client.put(f"/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["mechanics"], [])

    def test_edit_ticket_add_and_remove_mechanics(self):
        response = self.client.put(f"/service-tickets/{self.ticket_id}/edit", json={
            "add_ids": [self.mechanic_id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["mechanics"]), 1)
