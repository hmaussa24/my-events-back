from app.repositories.session_repository import SessionRepository
from fastapi import HTTPException, status

class DeleteSessionUseCase:
    def __init__(self, session_repo: SessionRepository):
        self.session_repo = session_repo

    def execute(self, session_id: int, current_user_id: int):
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        if session.speaker_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this session")

        self.session_repo.delete_session(session)