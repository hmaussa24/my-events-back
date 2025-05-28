# app/use_cases/user/create_user.py
from typing import Optional

from app.core.exceptions import HTTPException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import IUserRepository
from app.schemas.user import UserCreate, UserResponse # Importamos los esquemas de entrada y salida


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
        # Verificar si ya existe un usuario con el mismo email
        existing_user = self.user_repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        # Hashear la contraseña antes de guardar
        hashed_password = get_password_hash(user_in.password)

        # Crear una instancia del modelo de la base de datos
        # No pasamos el ID aquí, ya que la DB lo generará
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,        # Por defecto activo
            is_superuser=False     # Por defecto no superusuario
        )

        # Persistir el usuario usando el repositorio
        created_user = self.user_repository.create(db_user)

        # Retornar el usuario usando el esquema de respuesta
        return UserResponse.model_validate(created_user)