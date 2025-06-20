class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Chawgrizzly21!@localhost/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:Chawgrizzly21!@localhost/production_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
