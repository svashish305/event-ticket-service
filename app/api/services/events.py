from datetime import datetime
from sqlalchemy.orm import Session

from app.api.models import models
from app.api.schemas import schemas

def is_future_event(event_date_time):
    return event_date_time > datetime.now()

async def get_events(db: Session):
    events_out = []
    try:
        events = db.query(models.Event).all()
        for event in events:
            tickets = db.query(models.Ticket).filter(models.Ticket.event_id == event.id).all()
            num_available_tickets = sum([ticket.num_available for ticket in tickets])
            events_out.append(schemas.EventOut(
                name=event.name,
                description=event.description,
                date_time=event.date_time,
                num_available_tickets=num_available_tickets
            ))
    except Exception as e:
        print("Unable to get events due to: ", e)
    finally:
        return events_out