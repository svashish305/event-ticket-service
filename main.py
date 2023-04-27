from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

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
    new_reservation = crud.make_reservation(db, reservation)
    return new_reservation

@app.put("/reservations/{reservation_id}", response_model=schemas.ReservationOut)
def update_reservation(reservation_id: int, num_tickets: int, db: Session = Depends(get_db)):
    updated_reservation = crud.update_reservation(db, reservation_id, num_tickets)
    return updated_reservation

@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return crud.cancel_reservation(db, reservation_id)