from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemas import schemas
from app.api.dependencies import get_db
from app.api.services import events

router = APIRouter()

@router.get("/", response_model=list[schemas.EventOut])
async def get_events(db: Session = Depends(get_db)):
    all_events = await events.get_events(db)
    return all_events

