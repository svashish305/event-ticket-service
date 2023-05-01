from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import schemas
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.crud import crud

router = APIRouter()

@router.post("/", response_model=schemas.ReservationOut)
def make_reservation(reservation: schemas.ReservationIn, db: Session = Depends(get_db)):
    new_reservation = crud.make_reservation(reservation, db)
    if new_reservation.message:
        raise HTTPException(status_code=new_reservation.code, detail=new_reservation.message)
    return new_reservation

@router.put("/{reservation_id}", response_model=schemas.ReservationOut)
def update_reservation(reservation_id: int, num_tickets: int, db: Session = Depends(get_db)):
    updated_reservation = crud.update_reservation(reservation_id, num_tickets, db)
    if updated_reservation.message:
        raise HTTPException(status_code=updated_reservation.code, detail=updated_reservation.message)
    return updated_reservation

@router.delete("/{reservation_id}", response_model=schemas.ReservationOut)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    cancelled_reservation = crud.cancel_reservation(reservation_id, db)
    if cancelled_reservation.message:
        raise HTTPException(status_code=cancelled_reservation.code, detail=cancelled_reservation.message)
    return cancelled_reservation