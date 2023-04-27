from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas

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

def make_reservation(reservation: schemas.ReservationIn, db: Session):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == reservation.ticket_id).first()
    if ticket.num_available >= reservation.num_tickets:
        new_reservation = models.Reservation(ticket_id=reservation.ticket_id, num_reserved=reservation.num_tickets)
        db.add(new_reservation)
        ticket.num_available -= reservation.num_tickets
        db.commit()
        db.refresh(new_reservation)
        return new_reservation
    else:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
    
def update_reservation(reservation_id: int, num_tickets: int, db: Session):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation:
        ticket = reservation.ticket
        num_available = ticket.num_available + reservation.num_reserved
        if num_tickets <= num_available:
            ticket.num_available = num_available - num_tickets
            reservation.num_reserved = num_tickets
            db.commit()
            db.refresh(reservation)
            return reservation
        else:
            raise HTTPException(status_code=400, detail="Not enough tickets available")
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
def cancel_reservation(reservation_id: int, db: Session):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation:
        ticket = reservation.ticket
        ticket.num_available += reservation.num_reserved
        db.delete(reservation)
        db.commit()
        return {"message": "Reservation cancelled"}
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")