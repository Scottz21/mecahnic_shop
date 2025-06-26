from app.models import ServiceTicket
from app.extensions import ma

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True

class UpdateServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        exclude = ('mechanics',)  # Exclude mechanics from update schema
    
   
ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
UpdateServiceTicketSchema = UpdateServiceTicketSchema()
