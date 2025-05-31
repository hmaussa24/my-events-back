from typing import Optional

from sqlmodel import Session

from app.models.user import User
from app.repositories.base import SQLModelRepository, IBaseRepository


class IUserRepository(IBaseRepository[User]):
    """
    Interfaz específica para el repositorio de usuarios.
    Puede añadir métodos específicos de usuario aquí.
    """
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su dirección de email."""
        pass


class UserRepository(SQLModelRepository[User], IUserRepository):
    """
    Implementación del repositorio de usuarios usando SQLModel.
    """
    def __init__(self, session: Session):
        super().__init__(model=User, session=session)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_by_field("email", email)