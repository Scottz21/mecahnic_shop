from sqlalchemy import Date
from sqlalchemy.orm import mapped_column, Mapped
from typing import List
from app.extensions import db

# Association table
service_mechanics = db.Table(
    'service_mechanics',
    db.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(db.Model):  # using db.Model
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates="customer")

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[Date] = mapped_column(Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates="service_tickets")
    
    mechanics: Mapped[List['Mechanic']] = db.relationship(
        secondary=service_mechanics,
        back_populates="tickets"
    )

    # NEW RELATIONSHIP: Parts used on this ticket (with quantity via junction model)
    parts_assoc = db.relationship("TicketPart", back_populates="ticket", cascade="all, delete-orphan")


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    tickets: Mapped[List['ServiceTicket']] = db.relationship(
        secondary=service_mechanics,
        back_populates="mechanics"
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    tickets_assoc = db.relationship("TicketPart", back_populates="inventory", cascade="all, delete-orphan")

class TicketPart(db.Model):
    __tablename__ = 'ticket_parts'
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    ticket = db.relationship("ServiceTicket", back_populates="parts_assoc")
    inventory = db.relationship("Inventory", back_populates="tickets_assoc")
    
    
