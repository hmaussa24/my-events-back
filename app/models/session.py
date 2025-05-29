# app/models/session.py
from asyncio import Event
from datetime import datetime
from typing import Optional
#from app.models.user import User
from sqlmodel import Field, Relationship, SQLModel

# from app.models.event import Event # Asegúrate de importar Event
# \\from app.models.user import User # Asegúrate de importar User para el ponente (speaker)

class SessionBase(SQLModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    start_time: datetime
    end_time: datetime
    capacity: int = Field(ge=0)

    event_id: int = Field(foreign_key="event.id")
    speaker_id: int = Field(foreign_key="user.id") # El ponente es un usuario


class Session(SessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}, nullable=False)

    event: "Event" = Relationship(back_populates="sessions")
    speaker: "User" = Relationship(back_populates="sessions_as_speaker") #Los speakers son usuarios registrados