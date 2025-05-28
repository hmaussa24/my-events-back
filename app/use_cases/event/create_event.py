from datetime import datetime
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse
from app.models.envent import Event
from fastapi import HTTPException, status

class CreateEventUseCase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def execute(self, event_in: EventCreate, organizer_id: int) -> EventResponse:
        if event_in.event_date < datetime.now().date():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event date cannot be in the past")

        event = self.event_repo.create_event(event_in, organizer_id)
        return EventResponse.model_validate(event)