from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.models import models
from app.api.schemas import schemas
from .events import is_past_event

async def make_reservation(reservation: schemas.ReservationIn, db: Session):
    try:
        if reservation.num_tickets <= 0:
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Number of tickets must be greater than 0")
        db.begin()
        event = db.query(models.Event).filter(models.Event.id == reservation.event_id).first() or None
        if not event:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Event not found")
        if event.date_time and is_past_event(event.date_time):
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Event has already passed")
        if reservation.num_tickets > event.num_available:
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Not enough tickets available")
        new_reservation = models.Reservation(event_id=reservation.event_id, num_reserved=reservation.num_tickets)
        db.add(new_reservation)
        event.num_available -= reservation.num_tickets
        db.commit()
        return schemas.ReservationOut(id=new_reservation.id, event_id=new_reservation.event_id, num_reserved=new_reservation.num_reserved)
    except Exception as e:
        print("Unable to make reservation due to: ", e)
        db.rollback()
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to make reservation") 


async def update_reservation(reservation_id: int, num_tickets: int, operation: str, db: Session):
    try:
        if num_tickets <= 0:
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Number of tickets must be greater than 0")
        db.begin()
        reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first() or None
        if not reservation:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Reservation not found")
        event = reservation.event or None
        if not event:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Event not found")
        if event.date_time and is_past_event(event.date_time):
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Event has already passed")
        if operation == schemas.ReservationOperation.INCREMENT:
            if num_tickets > event.num_available:
                return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Not enough tickets available")
            updated_num_tickets = reservation.num_reserved + num_tickets
        elif operation == schemas.ReservationOperation.DECREMENT:
            if num_tickets > reservation.num_reserved:
                return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Number of tickets must be less than original number of tickets")
            updated_num_tickets = reservation.num_reserved - num_tickets
        
        updated_num_available = event.num_available + reservation.num_reserved - updated_num_tickets
        reservation.num_reserved = updated_num_tickets
        event.num_available = updated_num_available
        db.commit()
        return schemas.ReservationOut(id=reservation.id, event_id=reservation.event_id, num_reserved=reservation.num_reserved)
    except (IntegrityError, Exception) as e:
        db.rollback()
        print("Unable to update reservation due to: ", e)
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to update reservation")
    

async def cancel_reservation(reservation_id: int, db: Session):
    try:
        db.begin()
        reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first() or None
        if not reservation:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Reservation not found")
        event = reservation.event or None
        if not event:
            return schemas.ReservationOut(code=status.HTTP_404_NOT_FOUND, message="Event not found")
        if event.date_time and is_past_event(event.date_time):
            return schemas.ReservationOut(code=status.HTTP_400_BAD_REQUEST, message="Event has already passed")
        event.num_available += reservation.num_reserved
        db.delete(reservation)
        db.commit()
        return schemas.ReservationOut(code=status.HTTP_204_NO_CONTENT, message="Reservation cancelled")
    except (IntegrityError, Exception) as e:
        db.rollback()
        print("Unable to cancel reservation due to: ", e)
        return schemas.ReservationOut(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unable to cancel reservation")
    