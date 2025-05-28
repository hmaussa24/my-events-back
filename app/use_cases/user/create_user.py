from typing import Optional

from app.core.exceptions import HTTPException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import IUserRepository
from app.schemas.user import UserCreate, UserResponse


class CreateUserUseCase:
    """
    Caso de uso para crear un nuevo usuario.
    """
    def __init__(self, user_repository: IUserRepository):
        self.user_repository: IUserRepository = user_repository

    def execute(self, user_in: UserCreate) -> UserResponse:
        """
        Ejecuta la lógica para crear un usuario.
        Args:
            user_in (UserCreate): Datos del usuario a crear.
        Returns:
            UserResponse: El usuario creado.
        Raises:
            HTTPException: Si el email ya está registrado.
        """
        existing_user = self.user_repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )

        created_user = self.user_repository.create(db_user)
        return UserResponse.model_validate(created_user)