from flask import Flask
from .extensions import db, ma, limiter, cache
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import service_tickets_bp  
from .blueprints.customers import customers_bp
from .blueprints.inventory import inventory_bp
from flask_limiter.util import get_remote_address 
from flask_swagger_ui import get_swaggerui_blueprint  

from .config import DevelopmentConfig, TestingConfig, ProductionConfig

config_map = {
    "DevelopmentConfig": DevelopmentConfig,
    "TestingConfig": TestingConfig,
    "ProductionConfig": ProductionConfig
}

# Swagger UI config
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Shop API"} 
)

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Rate limit config
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
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app
