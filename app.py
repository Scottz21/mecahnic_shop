from app import create_app
from app.models import db

app = create_app('DevelopmentConfig')


with app.app_context():
   # db.drop_all()  # Drop all tables
    db.create_all()  # Create all tables
if __name__ == '__main__':
    app.run(debug=True)
