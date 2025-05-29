from typing import List, Optional
from sqlmodel import Session, select
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate

class SessionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_session(self, session_in: SessionCreate) -> Session:
        session = Session.model_validate(session_in)
        self.session.add(session)
        self.session.commit()
        self.session.refresh(session)
        return session

    def get_session_by_id(self, session_id: int) -> Optional[Session]:
        return self.session.get(Session, session_id)

    def get_sessions_by_event_id(self, event_id: int, skip: int = 0, limit: int = 100) -> List[Session]:
        statement = select(Session).where(Session.event_id == event_id).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update_session(self, session: Session, session_update: SessionUpdate) -> Session:
        update_data = session_update.model_dump(exclude_unset=True)
        session.sqlmodel_update(update_data)
        self.session.add(session)
        self.session.commit()
        self.session.refresh(session)
        return session

    def delete_session(self, session: Session):
        self.session.delete(session)
        self.session.commit()