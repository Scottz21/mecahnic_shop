from flask import Blueprint

mechanic_bp = Blueprint('mechanic', __name__)

# Import routes AFTER blueprint is created
from . import routes