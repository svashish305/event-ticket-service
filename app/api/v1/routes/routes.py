from fastapi import APIRouter, Request, Response
from app.api.v1.routes.endpoints import events, reservations

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

