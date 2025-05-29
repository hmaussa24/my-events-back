from typing import List, Optional
from app.repositories.event_repository import EventRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.event import EventResponse
from app.schemas.session import SessionResponse
from fastapi import HTTPException, status

class GetSessionUseCase:
    def __init__(self, session_repo: SessionRepository):
        self.session_repo = session_repo

    def execute_by_id(self, session_id: int) -> SessionResponse:
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionResponse.model_validate(session)
    
    def execute_all(self, event_id: int, skip: int = 0, limit: int = 100) -> List[SessionResponse]:
        sessions = self.session_repo.get_sessions_by_event_id(event_id, skip=skip, limit=limit)
        if not sessions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found for this event")
        return [SessionResponse.model_validate(session) for session in sessions]
