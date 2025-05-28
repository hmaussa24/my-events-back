from fastapi import APIRouter

from app.api.v1.endpoints import users
from app.api.v1.endpoints import events

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(events.router, tags=["events"])