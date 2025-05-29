from datetime import datetime, timezone
from app.repositories.event_repository import EventRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.session import SessionCreate, SessionResponse
from fastapi import HTTPException, status

class CreateSessionUseCase:
    def __init__(self, session_repo: SessionRepository):
        self.session_repo = session_repo

    def execute(self, session_in: SessionCreate) -> SessionResponse:
        start_time = session_in.start_time.astimezone(timezone.utc)
        end_time = session_in.end_time.astimezone(timezone.utc)
        if session_in.start_time.astimezone(timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session start time cannot be in the past")
        if end_time <= start_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session end time must be after start time")
        session = self.session_repo.create_session(session_in)
        return SessionResponse.model_validate(session)