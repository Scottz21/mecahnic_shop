from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp 
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import tickets_schema
from app.models import ServiceTicket


@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email, Customer.password == password)
    customer = db.session.execute(query).scalars().first()

    if customer:
        token = encode_token(customer.id)

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid email or password!"}), 401

# CREATE CUSTOMERS
@customers_bp.route('/', methods=['POST'])
@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Customer with this email already exists"}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# GET ALL CUSTOMERS
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

# GET CUSTOMER BY ID
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 400

# UPDATE CUSTOMER
@customers_bp.route("/<int:customer_id>", methods=['PUT'])
@limiter.limit("5 per month")
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 400

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

# DELETE CUSTOMER
@customers_bp.route("/", methods=['DELETE'])  
@token_required
@limiter.limit("5 per day")
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully."}), 200

# GET MY SERVICE TICKETS (requires token)
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return tickets_schema.jsonify(tickets), 200

