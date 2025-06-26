from flask import request, jsonify
from sqlalchemy import select, func
from marshmallow import ValidationError
from . import service_tickets_bp
from app.extensions import db
from app.models import ServiceTicket, Mechanic, service_mechanics
from .schemas import ticket_schema, tickets_schema

# CREATE Service Ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

# GET All Tickets (with optional pagination)
@service_tickets_bp.route('/', methods=['GET'])
def get_tickets():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(ServiceTicket)
        pagination = db.paginate(query, page=page, per_page=per_page)
        return jsonify(tickets_schema.dump(pagination.items)), 200

    except:
        # Fallback: return all tickets if pagination params are missing
        query = select(ServiceTicket)
        tickets = db.session.execute(query).scalars().all()
        return jsonify(tickets_schema.dump(tickets)), 200

# ASSIGN Mechanic to Ticket
@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return ticket_schema.jsonify(ticket)

# REMOVE Mechanic from Ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return ticket_schema.jsonify(ticket)

# EDIT Ticket (add/remove multiple mechanics)
@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket(ticket_id):
    data = request.get_json()
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    for mech_id in add_ids:
        mech = db.session.get(Mechanic, mech_id)
        if mech and mech not in ticket.mechanics:
            ticket.mechanics.append(mech)

    for mech_id in remove_ids:
        mech = db.session.get(Mechanic, mech_id)
        if mech and mech in ticket.mechanics:
            ticket.mechanics.remove(mech)

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

# ADD Inventory Part to Ticket (with quantity)
@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['POST'])
def add_part_to_ticket(ticket_id, part_id):
    from app.models import Inventory, TicketPart  # local import to avoid circular dependency

    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(part_id)

    data = request.get_json()
    quantity = data.get("quantity", 1)

    association = TicketPart.query.filter_by(ticket_id=ticket_id, inventory_id=part_id).first()
    if association:
        association.quantity += quantity
    else:
        new_link = TicketPart(ticket_id=ticket_id, inventory_id=part_id, quantity=quantity)
        db.session.add(new_link)

    db.session.commit()
    return jsonify({"message": "Part added to ticket"}), 200
