from typing import List, Optional
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventResponse
from fastapi import HTTPException, status

class GetEventUseCase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def execute_by_id(self, event_id: int) -> EventResponse:
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return EventResponse.model_validate(event)

    def execute_all(self, skip: int = 0, limit: int = 100) -> List[EventResponse]:
        events = self.event_repo.get_all_events(skip=skip, limit=limit)
        return [EventResponse.model_validate(event) for event in events]

    def execute_search_by_name(self, name_query: str, skip: int = 0, limit: int = 100) -> List[EventResponse]:
        events = self.event_repo.search_events_by_name(name_query=name_query, skip=skip, limit=limit)
        return [EventResponse.model_validate(event) for event in events]