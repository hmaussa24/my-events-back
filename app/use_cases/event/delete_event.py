from app.repositories.event_repository import EventRepository
from fastapi import HTTPException, status

class DeleteEventUseCase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def execute(self, event_id: int, current_user_id: int):
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        if event.organizer_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this event")

        self.event_repo.delete_event(event)