# app/repositories/base.py
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, Type, Dict, Any

from sqlmodel import Session, SQLModel, select

# Definimos un TypeVar para los modelos de SQLModel
ModelType = TypeVar("ModelType", bound=SQLModel)

class IBaseRepository(ABC, Generic[ModelType]):
    """
    Interfaz abstracta para un repositorio base. Define las operaciones CRUD básicas.
    """
    @abstractmethod
    def get(self, id: Any) -> Optional[ModelType]:
        """Obtiene un objeto por su ID."""
        pass

    @abstractmethod
    def get_by_field(self, field_name: str, field_value: Any) -> Optional[ModelType]:
        """Obtiene un objeto por el valor de un campo específico."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene una lista de objetos."""
        pass

    @abstractmethod
    def create(self, obj_in: ModelType) -> ModelType:
        """Crea un nuevo objeto."""
        pass

    @abstractmethod
    def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Actualiza un objeto existente."""
        pass

    @abstractmethod
    def delete(self, db_obj: ModelType) -> None:
        """Elimina un objeto."""
        pass


class SQLModelRepository(IBaseRepository[ModelType]):
    """
    Implementación concreta de un repositorio base usando SQLModel.
    """
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get(self, id: Any) -> Optional[ModelType]:
        return self.session.get(self.model, id)

    def get_by_field(self, field_name: str, field_value: Any) -> Optional[ModelType]:
        statement = select(self.model).where(getattr(self.model, field_name) == field_value)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        self.session.commit()
        self.session.refresh(obj_in)
        return obj_in

    def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        # Asegúrate de que obj_in sea un diccionario para los campos a actualizar
        for key, value in obj_in.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ModelType) -> None:
        self.session.delete(db_obj)
        self.session.commit()