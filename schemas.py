from pydantic import BaseModel
from datetime import datetime

class EventOut(BaseModel):
    name: str
    description: str
    date_time: datetime
    num_available_tickets: int

class ReservationIn(BaseModel):
    ticket_id: int
    num_tickets: int

class ReservationOut(BaseModel):
    id: int = None
    ticket_id: int = None
    num_reserved: int = None
    message: str = None
    code: int = None
