from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session

from app.database.connection import get_db_session
from app.core.dependencies import get_current_user
from app.repositories.session_repository import SessionRepository
from app.use_cases.session.create_session import CreateSessionUseCase
from app.use_cases.session.get_session import GetSessionUseCase
from app.use_cases.session.delete_session import DeleteSessionUseCase
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.schemas.user import UserResponse

router = APIRouter()

def get_session_repository(session: Annotated[Session, Depends(get_db_session)]) -> SessionRepository:
    return SessionRepository(session)

def get_create_session_use_case(session_repo: Annotated[SessionRepository, Depends(get_session_repository)]) -> CreateSessionUseCase:
    return CreateSessionUseCase(session_repo)

def get_get_session_use_case(session_repo: Annotated[SessionRepository, Depends(get_session_repository)]) -> GetSessionUseCase:
    return GetSessionUseCase(session_repo)

def get_delete_session_use_case(session_repo: Annotated[SessionRepository, Depends(get_session_repository)]) -> DeleteSessionUseCase:
    return DeleteSessionUseCase(session_repo)

@router.post("/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED, summary="Crear una nueva sesión")
async def create_session(
    session_in: SessionCreate,
    create_session_uc: Annotated[CreateSessionUseCase, Depends(get_create_session_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Crea una nueva sesión. Requiere autenticación.
    """
    return create_session_uc.execute(session_in)

@router.get("/sessions/{event_id}", response_model=List[SessionResponse], summary="Obtener todas las sesiones o buscar por nombre")
async def get_sessions(
    event_id: int,
    get_session_uc: Annotated[GetSessionUseCase, Depends(get_get_session_use_case)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100)
):
    """
    Obtiene una lista de sesiones. Permite búsqueda por nombre y paginación.
    """
    return get_session_uc.execute_all(event_id=event_id, skip=skip, limit=limit)

@router.get("/session/{session_id}", response_model=SessionResponse, summary="Obtener una sesión por ID")
async def get_session_by_id(
    session_id: int,
    get_session_uc: Annotated[GetSessionUseCase, Depends(get_get_session_use_case)]
):
    """
    Obtiene los detalles de una sesión específica por su ID.
    """
    return get_session_uc.execute_by_id(session_id)

@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una sesión")
async def delete_session(
    session_id: int,
    delete_session_uc: Annotated[DeleteSessionUseCase, Depends(get_delete_session_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Elimina una sesión. Solo el speaker o un superusuario pueden hacerlo.
    """
    delete_session_uc.execute(session_id, current_user.id)
    return