from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm


from app.database.connection import get_db_session
from app.core.dependencies import get_current_user, get_current_active_superuser
from app.repositories.user_repository import UserRepository
from app.use_cases.user.create_user import CreateUserUseCase
from app.use_cases.user.get_user import GetUserUseCase
from app.use_cases.user.login_user import LoginUserUseCase
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()

def get_user_repository(session: Annotated[Session, Depends(get_db_session)]) -> UserRepository:
    """Provee una instancia de UserRepository."""
    return UserRepository(session)

def get_create_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> CreateUserUseCase:
    """Provee una instancia de CreateUserUseCase."""
    return CreateUserUseCase(user_repo)

def get_get_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> GetUserUseCase:
    """Provee una instancia de GetUserUseCase."""
    return GetUserUseCase(user_repo)

def get_login_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> LoginUserUseCase:
    """Provee una instancia de LoginUserUseCase."""
    return LoginUserUseCase(user_repo)


@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo usuario")
async def create_user(
    user_in: UserCreate,
    create_user_uc: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)]
):
    """
    Crea un nuevo usuario en el sistema.
    """
    try:
        new_user = create_user_uc.execute(user_in)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

@router.post("/login/access-token", response_model=Token, summary="Obtener token de acceso JWT")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_user_uc: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)]
):
    """
    Autentica a un usuario y devuelve un token de acceso JWT.
    """
    try:
        user_login_data = UserLogin(email=form_data.username, password=form_data.password)
        token = login_user_uc.execute(user_login_data)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )


@router.get("/users/me", response_model=UserResponse, summary="Obtener información del usuario actual")
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Obtiene la información del usuario autenticado actualmente.
    Requiere autenticación JWT.
    """
    return current_user 


@router.get("/users/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID (solo superusuarios)")
async def read_user_by_id(
    user_id: int,
    get_user_uc: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
    current_user: Annotated[UserResponse, Depends(get_current_active_superuser)]
):
    """
    Obtiene la información de un usuario por su ID.
    Solo accesible por superusuarios.
    """
    try:
        user = get_user_uc.execute_by_id(user_id)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )