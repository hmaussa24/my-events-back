from datetime import datetime
from app.schemas.event import EventResponse
from app.schemas.user import UserResponse
from sqlmodel import SQLModel

class RegistrationCreate(SQLModel):
    event_id: int # El usuario que se registra ya está autenticado

class RegistrationResponse(SQLModel):
    id: int
    user_id: int
    event_id: int
    registration_date: datetime
    event: EventResponse
    user: UserResponse