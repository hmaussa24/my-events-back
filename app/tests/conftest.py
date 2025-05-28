# app/tests/conftest.py
import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from app.api.main import app
from app.database.connection import get_db_session # Importa nuestra función de dependencia
from app.models.user import User # Asegúrate de importar todos los modelos que vayas a probar

# Fixture para un motor de base de datos de prueba (SQLite en memoria)
@pytest.fixture(name="session")
def session_fixture():
    """
    Crea un motor de base de datos SQLite en memoria para pruebas.
    Crea las tablas, provee una sesión y luego las elimina.
    """
    # Usamos SQLite en memoria para la velocidad de las pruebas
    engine = create_engine("sqlite:///./test.db")
    # Alternativamente, para una base de datos en memoria completa
    # engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine) # Crea todas las tablas definidas por SQLModel
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Elimina las tablas al finalizar las pruebas


# Fixture para sobrescribir la dependencia de la sesión de DB en FastAPI
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Crea un cliente de prueba para FastAPI y sobrescribe la dependencia de DB
    para usar la sesión de prueba.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear() # Limpia las sobrescrituras después de la prueba

# Fixture para crear un usuario de prueba para login
@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Crea un usuario de prueba en la base de datos para pruebas de login."""
    from app.core.security import get_password_hash
    from app.models.user import User

    hashed_password = get_password_hash("testpassword")
    user = User(email="test@example.com", hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user