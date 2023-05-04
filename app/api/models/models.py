from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    date_time = Column(DateTime)
    reservations = relationship("Reservation", back_populates="event")
    num_available = Column(Integer)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="reservations")
    num_reserved = Column(Integer)
    version_id = Column(Integer, nullable=False)

    __mapper_args__ = {"version_id_col": version_id}