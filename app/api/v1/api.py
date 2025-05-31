from fastapi import APIRouter

from app.api.v1.endpoints import users
from app.api.v1.endpoints import events
from app.api.v1.endpoints import session
from app.api.v1.endpoints import registrations

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(events.router, tags=["events"])
api_router.include_router(session.router, tags=["sessions"])
api_router.include_router(registrations.router, tags=["registrations"])