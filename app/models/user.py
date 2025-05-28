# app/models/user.py
from typing import Optional
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel # Importamos Field para definir columnas y SQLModel para el ORM

class User(SQLModel, table=True):
    """
    Representa un usuario en la base de datos.
    'table=True' indica que esta clase mapea a una tabla en la DB.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True) # El email debe ser único y lo indexamos para búsquedas rápidas
    hashed_password: str # Almacenaremos la contraseña ya hasheada
    is_active: bool = Field(default=True) # Si la cuenta de usuario está activa
    is_superuser: bool = Field(default=False) # Si el usuario tiene privilegios de superusuario
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Puedes añadir más campos aquí, como:
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None

    class Config:
        """
        Configuración Pydantic para el modelo.
        """
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "supersecretpasswordhash", # En un caso real, no se expondría directamente
                "is_active": True,
                "is_superuser": False,
            }
        }