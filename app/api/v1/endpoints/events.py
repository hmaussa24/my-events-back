from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlmodel import Session

from app.database.connection import get_db_session
from app.core.dependencies import get_current_user
from app.repositories.event_repository import EventRepository
from app.use_cases.event.create_event import CreateEventUseCase
from app.use_cases.event.get_event import GetEventUseCase
from app.use_cases.event.update_event import UpdateEventUseCase
from app.use_cases.event.delete_event import DeleteEventUseCase
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.schemas.user import UserResponse


router = APIRouter()

def get_event_repository(session: Annotated[Session, Depends(get_db_session)]) -> EventRepository:
    return EventRepository(session)

def get_create_event_use_case(event_repo: Annotated[EventRepository, Depends(get_event_repository)]) -> CreateEventUseCase:
    return CreateEventUseCase(event_repo)

def get_get_event_use_case(event_repo: Annotated[EventRepository, Depends(get_event_repository)]) -> GetEventUseCase:
    return GetEventUseCase(event_repo)

def get_update_event_use_case(event_repo: Annotated[EventRepository, Depends(get_event_repository)]) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repo)

def get_delete_event_use_case(event_repo: Annotated[EventRepository, Depends(get_event_repository)]) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repo)


@router.post("/event", response_model=EventResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo evento")
async def create_event(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    create_event_uc: Annotated[CreateEventUseCase, Depends(get_create_event_use_case)],
    name: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    location: str = Form(...),
    capacity: int = Form(...),
    status: str = Form(...),
    image: UploadFile = File(...),
):
    """
    Crea un nuevo evento. Requiere autenticación. El usuario autenticado será el organizador.
    Permite subir una imagen del evento.
    """
    try:
        image_filename = f"event_{current_user.id}_{image.filename}"
        image_path = f"static/events/{image_filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        event_in = EventCreate(
            name=name,
            description=description,
            event_date=event_date,
            location=location,
            capacity=capacity,
            status=status,
        )
        return create_event_uc.execute(event_in, current_user.id, image=image_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/events", response_model=List[EventResponse], summary="Obtener todos los eventos o buscar por nombre")
async def get_events(
    get_event_uc: Annotated[GetEventUseCase, Depends(get_get_event_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    name_query: Optional[str] = Query(None, description="Buscar eventos por nombre o parte del nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100)
):
    """
    Obtiene una lista de eventos. Permite búsqueda por nombre y paginación.
    """
    try:
        if name_query:
            return get_event_uc.execute_search_by_name_by_user(name_query=name_query, current_user_id=current_user.id, skip=skip, limit=limit)
        return get_event_uc.execute_all_by_user(current_user_id=current_user.id, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/events/all", response_model=List[EventResponse], summary="Obtener todos los eventos o buscar por nombre")
async def get_events(
    get_event_uc: Annotated[GetEventUseCase, Depends(get_get_event_use_case)],
    name_query: Optional[str] = Query(None, description="Buscar eventos por nombre o parte del nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100)
):
    """
    Obtiene una lista de eventos. Permite búsqueda por nombre y paginación.
    """
    try:
        if name_query:
            return get_event_uc.execute_search_by_name(name_query=name_query, skip=skip, limit=limit)
        return get_event_uc.execute_all(skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/event/{event_id}", response_model=EventResponse, summary="Obtener un evento por ID")
async def get_event_by_id(
    event_id: int,
    get_event_uc: Annotated[GetEventUseCase, Depends(get_get_event_use_case)]
):
    """
    Obtiene los detalles de un evento específico por su ID.
    """
    try:
        return get_event_uc.execute_by_id(event_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.patch("/event/{event_id}", response_model=EventResponse, summary="Actualizar un evento")
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    update_event_uc: Annotated[UpdateEventUseCase, Depends(get_update_event_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Actualiza la información de un evento. Solo el organizador del evento o un superusuario pueden hacerlo.
    """
    try:
        return update_event_uc.execute(event_id, event_update, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.delete("/event/{event_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un evento")
async def delete_event(
    event_id: int,
    delete_event_uc: Annotated[DeleteEventUseCase, Depends(get_delete_event_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Elimina un evento. Solo el organizador del evento o un superusuario pueden hacerlo.
    """
    try:
        delete_event_uc.execute(event_id, current_user.id)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")