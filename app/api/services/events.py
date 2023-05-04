from datetime import datetime
from sqlalchemy.orm import Session

from app.api.models import models
from app.api.schemas import schemas

def is_past_event(event_date_time):
    return event_date_time < datetime.now()

async def get_events(db: Session):
    events = []
    try:
        all_events = db.query(models.Event).order_by(models.Event.id.asc()).all() or []
        events = [
            schemas.EventOut(
                id=event.id, 
                name=event.name, 
                description=event.description, 
                date_time=event.date_time, 
                num_available=event.num_available
            ) for event in all_events
        ]
    except Exception as e:
        print("Unable to get events due to: ", e)
    finally:
        return events