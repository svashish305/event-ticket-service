from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request):
    return request.state.db

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/events/", response_model=list[schemas.EventOut])
def get_events(db: Session = Depends(get_db)):
    events = crud.get_events(db)
    return events

@app.post("/reservations/", response_model=schemas.ReservationOut)
def make_reservation(reservation: schemas.ReservationIn, db: Session = Depends(get_db)):
    new_reservation = crud.make_reservation(reservation, db)
    if new_reservation.message:
        raise HTTPException(status_code=new_reservation.code, detail=new_reservation.message)
    return new_reservation

@app.put("/reservations/{reservation_id}", response_model=schemas.ReservationOut)
def update_reservation(reservation_id: int, num_tickets: int, db: Session = Depends(get_db)):
    updated_reservation = crud.update_reservation(reservation_id, num_tickets, db)
    if updated_reservation.message:
        raise HTTPException(status_code=updated_reservation.code, detail=updated_reservation.message)
    return updated_reservation

@app.delete("/reservations/{reservation_id}", response_model=schemas.ReservationOut)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    cancelled_reservation = crud.cancel_reservation(reservation_id, db)
    if cancelled_reservation.message:
        raise HTTPException(status_code=cancelled_reservation.code, detail=cancelled_reservation.message)
    return cancelled_reservation