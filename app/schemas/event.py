from datetime import date, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

from app.models.envent import EventStatus

class EventBase(SQLModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_date: date
    location: str = Field(max_length=200)
    capacity: int = Field(ge=0)
    status: EventStatus = Field(default=EventStatus.DRAFT)

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_date: Optional[date] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=200)
    capacity: Optional[int] = Field(default=None, ge=0)
    status: Optional[EventStatus] = Field(default=None)

class EventResponse(EventBase):
    id: int
    organizer_id: int
    created_at: datetime
    updated_at: datetime