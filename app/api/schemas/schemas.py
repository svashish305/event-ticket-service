from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class EventOut(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    date_time: datetime = None
    num_available: int = None

class ReservationIn(BaseModel):
    event_id: int
    num_tickets: int

class ReservationOperation(str, Enum):
    INCREMENT = 'increase number of tickets'
    DECREMENT = 'decrease number of tickets'

class ReservationUpdate(BaseModel):
    num_tickets: int
    operation: Optional[ReservationOperation] = None

class ReservationOut(BaseModel):
    id: int = None
    event_id: int = None
    num_reserved: int = None
    message: str = None
    code: int = None
