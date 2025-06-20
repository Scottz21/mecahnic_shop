from app.models import ServiceTicket
from app.extensions import ma

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
