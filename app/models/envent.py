from datetime import datetime, date
from typing import List, Optional
from enum import Enum as PyEnum

from app.models.user import User
from sqlmodel import Field, Relationship, SQLModel


class EventStatus(str, PyEnum):
    """Estados posibles de un evento."""
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class EventBase(SQLModel):
    """Base para la creación y actualización de eventos."""
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_date: date
    location: str = Field(max_length=200)
    capacity: int = Field(ge=0)
    status: EventStatus = Field(default=EventStatus.DRAFT)

    organizer_id: int = Field(foreign_key="user.id")


class Event(EventBase, table=True):
    """Modelo de la tabla 'events'."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False) # Para PostgreSQL, considera `server_default=text("now()")` o similar
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}, nullable=False)
    organizer: "User" = Relationship(back_populates="events")
    ##sessions: List["Session"] = Relationship(back_populates="event")
    ##registrations: List["Registration"] = Relationship(back_populates="event")