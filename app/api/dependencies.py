from fastapi import Request, Response
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db(request: Request) -> Session:
    return request.state.db