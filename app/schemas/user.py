# app/schemas/user.py
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import Field, SQLModel
from datetime import datetime

# ====================================================================
# Esquemas Base (para herencia y reutilización)
# ====================================================================

# Modelo base para la creación de un usuario (campos obligatorios)
class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255) # Usamos EmailStr para validación de formato de email
    # No incluimos la contraseña aquí por seguridad; se manejará en UserCreate

# ====================================================================
# Esquemas para la entrada de datos de la API (Request Models)
# ====================================================================

# Esquema para crear un nuevo usuario (incluye contraseña en texto plano)
class UserCreate(UserBase):
    password: str = Field(min_length=8) # Contraseña en texto plano para la creación

# Esquema para iniciar sesión
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para actualizar un usuario (todos los campos opcionales)
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

# ====================================================================
# Esquemas para la salida de datos de la API (Response Models)
# ====================================================================

# Esquema para la respuesta de un usuario (no incluye la contraseña hasheada)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
            "is_superuser": False,
            "created_at": "2025-05-28T10:00:00.000Z",
            "updated_at": "2025-05-28T10:00:00.000Z",
        }
    })

# ====================================================================
# Esquemas para Autenticación JWT
# ====================================================================

# Esquema para el token JWT de acceso
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(json_schema_extra={ # <-- CAMBIO AQUI
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
        }
    })
    # class Config: # <-- ELIMINA O COMENTA ESTO
    #     json_schema_extra = { # <-- y esto
    #         "example": {
    #             "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    #             "token_type": "bearer",
    #         }
    #     }

# Esquema para los datos que se guardan dentro del token (payload)
class TokenPayload(BaseModel):
    sub: Optional[int] = None # 'sub' (subject) típicamente es el ID del usuario