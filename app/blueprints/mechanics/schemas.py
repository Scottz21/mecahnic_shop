from app.models import Mechanic, ServiceTicket
from app.extensions import ma
from marshmallow import fields

# Basic version (used in most cases, avoids recursion)
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        fields = ("id", "name", "email", "phone", "salary")  # Explicitly define public fields

    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

