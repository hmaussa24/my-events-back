from asyncio import Event
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    event_id: int = Field(foreign_key="event.id", index=True)
    registration_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(back_populates="registrations")
    event: "Event" = Relationship(back_populates="registrations")