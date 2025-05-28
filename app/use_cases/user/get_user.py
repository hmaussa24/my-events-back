# app/use_cases/user/get_user.py
from typing import Optional

from app.core.exceptions import HTTPException
from app.models.user import User
from app.repositories.user_repository import IUserRepository
from app.schemas.user import UserResponse


class GetUserUseCase:
    """
    Caso de uso para obtener información de un usuario.
    """
    def __init__(self, user_repository: IUserRepository):
        self.user_repository: IUserRepository = user_repository

    def execute_by_id(self, user_id: int) -> UserResponse:
        """
        Obtiene un usuario por su ID.
        Args:
            user_id (int): ID del usuario.
        Returns:
            UserResponse: El usuario encontrado.
        Raises:
            HTTPException: Si el usuario no es encontrado.
        """
        user = self.user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    def execute_by_email(self, email: str) -> UserResponse:
        """
        Obtiene un usuario por su email.
        Args:
            email (str): Email del usuario.
        Returns:
            UserResponse: El usuario encontrado.
        Raises:
            HTTPException: Si el usuario no es encontrado.
        """
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)