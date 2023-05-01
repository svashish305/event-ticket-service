from fastapi import APIRouter, Depends
from app.api.schemas import schemas
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.crud import crud

router = APIRouter()

@router.get("/", response_model=list[schemas.EventOut])
def get_events(db: Session = Depends(get_db)):
    events = crud.get_events(db)
    return events

