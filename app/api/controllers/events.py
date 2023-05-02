from fastapi import APIRouter, Depends
from app.api.schemas import schemas
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.services import events

router = APIRouter()

@router.get("/", response_model=list[schemas.EventOut])
def get_events(db: Session = Depends(get_db)):
    all_events = events.get_events(db)
    return all_events

