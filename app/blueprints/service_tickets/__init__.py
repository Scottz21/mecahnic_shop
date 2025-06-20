from flask import Blueprint

service_ticket_bp = Blueprint('service_ticket', __name__)

# Import routes AFTER blueprint is created
from . import routes