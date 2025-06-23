from flask import Blueprint


service_ticket_bp = Blueprint('service_ticket_bp', __name__)

from . import routes  # ensures the routes register
service_ticket_bp = Blueprint('service_ticket', __name__)

# Import routes AFTER blueprint is created
from . import routes