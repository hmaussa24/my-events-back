from datetime import datetime
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventUpdate, EventResponse
from app.models.envent import EventStatus
from fastapi import HTTPException, status

class UpdateEventUseCase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def execute(self, event_id: int, event_update: EventUpdate, current_user_id: int) -> EventResponse:
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        if event.organizer_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this event")

        if event_update.event_date and event_update.event_date < datetime.now().date():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event date cannot be in the past")

        if event.status == EventStatus.COMPLETED and event_update.status and event_update.status != EventStatus.COMPLETED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change status from completed")

        updated_event = self.event_repo.update_event(event, event_update)
        return EventResponse.model_validate(updated_event)