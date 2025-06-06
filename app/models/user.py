from asyncio import Event
from typing import Optional
from datetime import datetime

from app.models.registration import Registration
from app.models.session import Session
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    """
    Representa un usuario en la base de datos.
    'table=True' indica que esta clase mapea a una tabla en la DB.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    events: list["Event"] = Relationship(back_populates="organizer")
    sessions_as_speaker: list["Session"] = Relationship(back_populates="speaker")
    registrations: list["Registration"] = Relationship(back_populates="user")