from flask import jsonify, request
from . import inventory_bp
from app.models import db, Inventory
from .schemas import inventory_schema, inventories_schema

@inventory_bp.route('/', methods=['POST'])
def create_part():
    data = request.get_json()
    new_part = Inventory(**data)
    db.session.add(new_part)
    db.session.commit()
    return jsonify({
        "message": "Part created successfully",
        "part": inventory_schema.dump(new_part)
    }), 201

@inventory_bp.route('/', methods=['GET'])
def get_parts():
    parts = Inventory.query.all()
    return jsonify({
        "message": f"{len(parts)} parts retrieved",
        "parts": inventories_schema.dump(parts)
    }), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return jsonify({
        "message": "Part updated successfully",
        "part": inventory_schema.dump(part)
    }), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted successfully"}), 200
