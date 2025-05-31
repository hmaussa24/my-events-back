from fastapi import Depends, HTTPException, status
from datetime import timedelta

from app.core.exceptions import HTTPException
from app.core.security import verify_password, create_access_token, decode_access_token
from app.models.user import User
from app.repositories.user_repository import IUserRepository
from app.schemas.user import UserLogin, Token

from typing import Annotated
from jose import JWTError
from pydantic import ValidationError
from sqlmodel import Session

from app.core.security import decode_access_token
from app.database.connection import get_db_session
from app.models.user import User 
from app.schemas.user import TokenPayload



class LoginUserUseCase:
    """
    Caso de uso para el inicio de sesión de un usuario.
    """
    def __init__(self, user_repository: IUserRepository):
        self.user_repository: IUserRepository = user_repository

    def execute(self, user_login: UserLogin) -> Token:
        """
        Ejecuta la lógica de inicio de sesión.
        Args:
            user_login (UserLogin): Credenciales del usuario (email, password).
        Returns:
            Token: El token de acceso JWT si la autenticación es exitosa.
        Raises:
            HTTPException: Si las credenciales son inválidas o el usuario inactivo.
        """
        user = self.user_repository.get_by_email(user_login.email)

        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        access_token = create_access_token(
            subject=user.id,
        )
        refresh_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(days=1)
        )

        return Token(access_token=access_token, refresh_token=refresh_token)

    def refresh_access_token(self, refresh_token: str, db_session: Annotated[Session, Depends(get_db_session)],) -> Token:
        """
        Valida el refresh token y genera un nuevo access token si es válido.
        """
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if refresh_token.startswith("Bearer "):
            refresh_token = refresh_token.split(" ")[1]
        try:
            payload = decode_access_token(refresh_token)
            token_data = TokenPayload.model_validate(payload)
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = db_session.get(User, token_data.sub)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        try:
            access_token = create_access_token(subject=user.id)
            return Token(access_token=access_token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")