# app/schemas/session.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class SessionBase(SQLModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    start_time: datetime
    end_time: datetime
    capacity: int = Field(ge=0)
    event_id: int
    speaker_id: int

class SessionCreate(SessionBase):
    pass

class SessionUpdate(SessionBase):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)
    capacity: Optional[int] = Field(default=None, ge=0)
    event_id: Optional[int] = Field(default=None) 
    speaker_id: Optional[int] = Field(default=None)

class SessionResponse(SessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Introducción a FastAPI",
                "description": "Una sesión introductoria sobre FastAPI.",
                "start_time": "2025-05-28T10:00:00.000Z",
                "end_time": "2025-05-28T11:00:00.000Z",
                "capacity": 100,
                "event_id": 1,
                "speaker_id": 1,
                "created_at": "2025-05-28T09:00:00.000Z",
                "updated_at": "2025-05-28T09:30:00.000Z",
            }
        }   
    # Puedes añadir aquí información del ponente (UserResponse) o del evento (EventResponse)