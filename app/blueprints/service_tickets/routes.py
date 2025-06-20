from flask import request, jsonify
from app.models import db, Mechanic, ServiceTicket
from .schemas import ticket_schema, tickets_schema
from app.blueprints.service_tickets import service_ticket_bp

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@service_ticket_bp.route('/', methods=['GET'])
def get_tickets():
    all_tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(all_tickets)

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return ticket_schema.jsonify(ticket)

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return ticket_schema.jsonify(ticket)