from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.models import db, Mechanic
from .schemas import mechanic_schema, mechanics_schema
from . import mechanic_bp  # Use this blueprint
from app.models import db, Mechanic, service_mechanics
from sqlalchemy import select

# CREATE Mechanic
@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    new_mechanic = Mechanic(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

# GET All Mechanics (with optional pagination)
@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        pagination = db.paginate(query, page=page, per_page=per_page)
        return jsonify(mechanics_schema.dump(pagination.items)), 200

    except:
        # Fallback: return all mechanics if pagination params are missing
        query = select(Mechanic)
        mechanics = db.session.execute(query).scalars().all()
        return jsonify(mechanics_schema.dump(mechanics)), 200


# UPDATE Mechanic
@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

# DELETE Mechanic
@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return '', 204

# MOST ACTIVE Mechanics by ticket count
@mechanic_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    query = (
        db.session.query(Mechanic, func.count(service_mechanics.c.ticket_id).label("ticket_count"))
        .join(service_mechanics)
        .group_by(Mechanic.id)
        .order_by(func.count(service_mechanics.c.ticket_id).desc())
    )

    mechanics = [row[0] for row in query.all()]
    return mechanics_schema.jsonify(mechanics), 200

