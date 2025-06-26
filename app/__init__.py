from flask import Flask
from .extensions import db, ma, limiter, cache
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_tickets_bp  
from .blueprints.customers import customers_bp
from flask_limiter.util import get_remote_address 
from .blueprints.inventory import inventory_bp

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set rate limit config in app.config
    app.config["RATELIMIT_DEFAULT"] = "100 per hour"
    app.config["RATELIMIT_KEY_FUNC"] = get_remote_address

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)  

    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    with app.app_context():
        db.create_all()

    return app
