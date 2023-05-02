from fastapi import FastAPI, Request, Depends
from app.api.v1.routes import api_router
from app.core.config import settings
from app.api.dependencies import db_session_middleware, get_db

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
async def health_check():
    return {"status": "up"}

@app.middleware("http")
async def middleware_wrapper(request: Request, call_next):
    return await db_session_middleware(request, call_next)

app.include_router(api_router, prefix=settings.API_V1_STR, dependencies=[Depends(get_db)])