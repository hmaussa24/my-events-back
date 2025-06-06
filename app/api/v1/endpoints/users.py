from typing import Annotated

from app.core.config import Settings
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

@router.post("/login/access-token", summary="Obtener token de acceso JWT")
async def login_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_user_uc: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)]
):
    """
    Autentica a un usuario y devuelve un token de acceso JWT.
    """
    try:
        user_login_data = UserLogin(email=form_data.username, password=form_data.password)
        token = login_user_uc.execute(user_login_data)
        response = JSONResponse(
            content={
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "token_type": "bearer"
            },
            status_code=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=token.access_token, 
            httponly=True, 
            secure=True,
            samesite="Lax",
            max_age= 15 * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=token.refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7*24*60*60
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

@router.post("/login/refresh-token", summary="Obtener un nuevo access token usando refresh token")
async def refresh_access_token(
    response: Response,
    request: Request,
    login_user_uc: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)]
):
    """
    Recibe un refresh token válido y devuelve un nuevo access token JWT.
    """
    try:
        token = login_user_uc.refresh_access_token(request.cookies.get("refresh_token"))
        response = JSONResponse(
            content={
                "access_token": token.access_token,
                "token_type": "bearer"
            },
            status_code=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=15 * 60
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )

@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Cierre de sesión exitoso"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.get("/users/me", response_model=UserResponse, summary="Obtener información del usuario actual")
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """
    Obtiene la información del usuario autenticado actualmente.
    Requiere autenticación JWT.
    """
    try:
        return current_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}"
        )