from sqlalchemy.orm import Session

from app.api.models import models
from app.api.schemas import schemas

def get_events(db: Session):
    events = db.query(models.Event).all()
    events_out = []
    for event in events:
        tickets = db.query(models.Ticket).filter(models.Ticket.event_id == event.id).all()
        num_available_tickets = sum([ticket.num_available for ticket in tickets])
        events_out.append(schemas.EventOut(
            name=event.name,
            description=event.description,
            date_time=event.date_time,
            num_available_tickets=num_available_tickets
        ))
    return events_out