from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from app.repositories.registration import RegistrationRepository
from app.repositories.event_repository import EventRepository
from app.use_cases.registrations.register_for_events import RegisterForEvent
from app.use_cases.registrations.get_user_registrations import GetUserRegistrations
from app.use_cases.registrations.get_user_event_registrations import GetUserEventRegistrations
from app.schemas.registration import RegistrationResponse
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.database.connection import get_db_session
from sqlmodel import Session

router = APIRouter()

def get_registration_repository(session: Annotated[Session, Depends(get_db_session)]) -> RegistrationRepository:
    return RegistrationRepository(session)

def get_event_repository(session: Annotated[Session, Depends(get_db_session)]) -> EventRepository:
    return EventRepository(session)

def get_register_for_event_use_case(
    registration_repo: Annotated[RegistrationRepository, Depends(get_registration_repository)],
    event_repo: Annotated[EventRepository, Depends(get_event_repository)]
) -> RegisterForEvent:
    return RegisterForEvent(registration_repo, event_repo)

def get_get_user_registrations_use_case(
    registration_repo: Annotated[RegistrationRepository, Depends(get_registration_repository)]
) -> GetUserRegistrations:
    return GetUserRegistrations(registration_repo)

def get_get_user_event_registrations_use_case(
    registration_repo: Annotated[RegistrationRepository, Depends(get_registration_repository)]
) -> GetUserEventRegistrations:
    return GetUserEventRegistrations(registration_repo)

@router.post("/event/{event_id}/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED, summary="Registrar usuario en evento")
async def register_for_event(
    event_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    register_for_event_uc: Annotated[RegisterForEvent, Depends(get_register_for_event_use_case)]
):
    """
    Registra al usuario autenticado en el evento especificado.
    """
    try:
        registration = register_for_event_uc.execute(current_user.id, event_id)
        return RegistrationResponse.model_validate(registration)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/event/{event_id}/registrations", response_model=List[RegistrationResponse], summary="Obtener usuarios registrados en un evento")
async def get_event_registrations(
    event_id: int,
    get_user_registrations_uc: Annotated[GetUserRegistrations, Depends(get_get_user_registrations_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Obtiene todos los usuarios registrados en un evento.
    """
    return get_user_registrations_uc.execute(event_id)

@router.get("/user/registrations", response_model=List[RegistrationResponse], summary="Obtener eventos a los que el usuario está registrado")
async def get_user_event_registrations(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    get_user_event_registrations_uc: Annotated[GetUserEventRegistrations, Depends(get_get_user_event_registrations_use_case)]
):
    """
    Obtiene todos los eventos a los que el usuario autenticado está registrado.
    """
    return get_user_event_registrations_uc.execute(current_user.id)