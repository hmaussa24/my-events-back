from typing import List, Optional
from sqlmodel import Session, select
from app.models.registration import Registration
from sqlalchemy import func

class RegistrationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_registration(self, user_id: int, event_id: int) -> Registration:
        registration = Registration(user_id=user_id, event_id=event_id)
        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)
        return registration

    def get_registration(self, user_id: int, event_id: int) -> Optional[Registration]:
        statement = select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
        return self.session.exec(statement).first()

    def get_registrations_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Registration]:
        statement = select(Registration).where(Registration.user_id == user_id).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_event_current_registrations_count(self, event_id: int) -> int:
        statement = select(func.count(Registration.id)).where(Registration.event_id == event_id)
        result = self.session.exec(statement).one_or_none()
        if result is None:
            return 0
        if isinstance(result, tuple):
            return result[0]
        return result
    
    def delete_registration(self, registration: Registration):
        self.session.delete(registration)
        self.session.commit()

    def get_registrations_by_event(self, event_id: int) -> List[Registration]:
        statement = select(Registration).where(Registration.event_id == event_id)
        return self.session.exec(statement).all()