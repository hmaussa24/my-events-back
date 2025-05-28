# app/tests/unit/use_cases/test_create_user.py
import pytest
from unittest.mock import MagicMock

from app.use_cases.user.create_user import CreateUserUseCase
from app.repositories.user_repository import IUserRepository # Importa la interfaz
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User # Necesitamos el modelo User para el mock
from app.core.exceptions import HTTPException # Para probar excepciones

def test_create_user_success():
    """
    Prueba que un usuario se crea correctamente.
    """
    mock_user_repo = MagicMock(spec=IUserRepository) # Mockea la interfaz del repositorio
    use_case = CreateUserUseCase(user_repository=mock_user_repo)

    user_data = UserCreate(email="test@example.com", password="SecurePassword123")

    # Configuramos el mock para simular el comportamiento esperado
    mock_user_repo.get_by_email.return_value = None # No existe un usuario con ese email
    mock_user_repo.create.return_value = User(
        id=1,
        email="test@example.com",
        hashed_password="mocked_hashed_password", # La contraseña hasheada
        is_active=True,
        is_superuser=False
    )

    # Ejecutamos el caso de uso
    result = use_case.execute(user_data)

    # Verificamos las aserciones
    assert result.email == user_data.email
    assert result.id == 1
    assert result.is_active is True
    assert result.is_superuser is False
    mock_user_repo.get_by_email.assert_called_once_with(user_data.email)
    mock_user_repo.create.assert_called_once() # Se llamó al método create


def test_create_user_email_exists():
    """
    Prueba que se lanza una excepción si el email ya existe.
    """
    mock_user_repo = MagicMock(spec=IUserRepository)
    use_case = CreateUserUseCase(user_repository=mock_user_repo)

    user_data = UserCreate(email="existing@example.com", password="Password123")

    # Configuramos el mock para simular que el email ya existe
    mock_user_repo.get_by_email.return_value = User(
        id=1, email="existing@example.com", hashed_password="abc"
    )

    # Esperamos que se lance una HTTPException
    with pytest.raises(HTTPException) as excinfo:
        use_case.execute(user_data)

    assert excinfo.value.status_code == 400
    assert "already exists" in excinfo.value.detail
    mock_user_repo.get_by_email.assert_called_once_with(user_data.email)
    mock_user_repo.create.assert_not_called() # Aseguramos que no se intentó crear