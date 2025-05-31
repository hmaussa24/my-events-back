from typing import List, Optional
from sqlmodel import Session, select
from app.models.envent import Event
from app.schemas.event import EventCreate, EventUpdate, EventStatus

class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event_in: EventCreate, organizer_id: int, image: str) -> Event:
        event = Event.model_validate(event_in, update={"organizer_id": organizer_id, "image_url": image})
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        return self.session.get(Event, event_id)

    def get_all_events_by_user(self, current_user_id: int, skip: int = 0, limit: int = 100) -> List[Event]:
        statement = select(Event).where(Event.organizer_id == current_user_id).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def search_events_by_name_by_user(self, name_query: str, current_user_id: int, skip: int = 0, limit: int = 100) -> List[Event]:
        statement = select(Event).where(Event.name.ilike(f"%{name_query}%"), Event.organizer_id == current_user_id).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def get_all_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        statement = select(Event).where(Event.status == EventStatus.PUBLISHED).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def search_events_by_name(self, name_query: str, skip: int = 0, limit: int = 100) -> List[Event]:
        statement = select(Event).where(Event.name.ilike(f"%{name_query}%"), Event.status == EventStatus.PUBLISHED).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update_event(self, event: Event, event_update: EventUpdate) -> Event:
        update_data = event_update.model_dump(exclude_unset=True)
        event.sqlmodel_update(update_data)
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete_event(self, event: Event):
        self.session.delete(event)
        self.session.commit()