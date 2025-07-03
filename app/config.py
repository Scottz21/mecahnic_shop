class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Chawgrizzly21!@localhost/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:Chawgrizzly21!@localhost/production_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
