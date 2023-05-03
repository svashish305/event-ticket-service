from fastapi import status
from sqlalchemy.orm import Session

from app.api.models import models
from app.api.schemas import schemas
from .events import is_future_event

async def make_reservation(reservation: schemas.ReservationIn, db: Session):
    try:
        db.begin()
        ticket = db.query(models.Ticket).filter(models.Ticket.id == reservation.ticket_id).first()
        event = db.query(models.Event).filter(models.Event.id == ticket.event_id).first()
        if ticket.num_available >= reservation.num_tickets and is_future_event(event.date_time):
            new_reservation = models.Reservation(ticket_id=reservation.ticket_id, num_reserved=reservation.num_tickets)
            db.add(new_reservation)
            ticket.num_available -= reservation.num_tickets
            db.commit()
            db.refresh(new_reservation)
            return schemas.ReservationOut(id=new_reservation.id, ticket_id=new_reservation.ticket_id, num_reserved=new_reservation.num_reserved)
        else:
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Not enough tickets available")
    except Exception as e:
        print("Unable to make reservation due to: ", e)
        db.rollback()
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to make reservation") 


async def update_reservation(reservation_id: int, num_tickets: int, db: Session):
    try:
        db.begin()
        reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
        ticket = db.query(models.Ticket).filter(models.Ticket.id == reservation.ticket_id).first()
        event = db.query(models.Event).filter(models.Event.id == ticket.event_id).first()
        if reservation and is_future_event(event.date_time):
            ticket = reservation.ticket
            num_available = ticket.num_available + reservation.num_reserved
            if num_tickets <= num_available:
                ticket.num_available = num_available - num_tickets
                reservation.num_reserved = num_tickets
                db.commit()
                db.refresh(reservation)
                return schemas.ReservationOut(id=reservation.id, ticket_id=reservation.ticket_id, num_reserved=reservation.num_reserved)
            else:
                return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Not enough tickets available")
        else:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Reservation not found")
    except Exception as e:
        print("Unable to update reservation due to: ", e)
        db.rollback()
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to update reservation")
    

async def cancel_reservation(reservation_id: int, db: Session):
    try:
        db.begin()
        reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
        ticket = db.query(models.Ticket).filter(models.Ticket.id == reservation.ticket_id).first()
        event = db.query(models.Event).filter(models.Event.id == ticket.event_id).first()
        if reservation and is_future_event(event.date_time):
            ticket = reservation.ticket
            ticket.num_available += reservation.num_reserved
            db.delete(reservation)
            db.commit()
            return schemas.ReservationOut(code=status.HTTP_204_NO_CONTENT, message="Reservation cancelled")
        else:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Reservation not found")
    except Exception as e:
        print("Unable to cancel reservation due to: ", e)
        db.rollback()
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to cancel reservation")
    