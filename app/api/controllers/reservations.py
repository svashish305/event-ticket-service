from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemas import schemas
from app.api.dependencies import get_db
from app.api.services import reservations

router = APIRouter()

@router.post("/", response_model=schemas.ReservationOut, status_code=status.HTTP_201_CREATED)
async def make_reservation(reservation: schemas.ReservationIn, db: Session = Depends(get_db)):
    new_reservation = await reservations.make_reservation(reservation, db)
    if new_reservation.message:
        raise HTTPException(status_code=new_reservation.code, detail=new_reservation.message)
    return new_reservation

@router.put("/{reservation_id}", response_model=schemas.ReservationOut)
async def update_reservation(reservation_id: int, request: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    updated_reservation = await reservations.update_reservation(reservation_id, request.num_tickets, request.operation, db)
    if updated_reservation.message:
        raise HTTPException(status_code=updated_reservation.code, detail=updated_reservation.message)
    return updated_reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    cancelled_reservation = await reservations.cancel_reservation(reservation_id, db)
    if cancelled_reservation.message:
        raise HTTPException(status_code=cancelled_reservation.code, detail=cancelled_reservation.message)