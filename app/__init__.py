from flask import Flask
from .extensions import db, ma
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_ticket_bp
from .blueprints.customers import customers_bp  # fixed relative import

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    # Register Blueprints *inside* the function
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(customers_bp, url_prefix='/customers')

    with app.app_context():
        db.create_all()

    return app
