from app.models import ServiceTicket, Mechanic
from app.extensions import ma
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        fields = ("id", "name", "email", "phone", "salary")  # Only expose relevant fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True

class UpdateServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        exclude = ('mechanics',)

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
update_ticket_schema = UpdateServiceTicketSchema()
