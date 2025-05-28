from typing import Optional

from app.core.exceptions import HTTPException
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repository import IUserRepository
from app.schemas.user import UserLogin, Token


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

        return Token(access_token=access_token)