from typing import Generator

from sqlmodel import create_engine, Session
from app.core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Función para crear todas las tablas definidas por SQLModel.
    Normalmente, esto se usa para pruebas o desarrollo inicial.
    En producción, preferimos Alembic para migraciones.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Abre y cierra la sesión por cada solicitud.
    """
    with Session(engine) as session:
        yield session