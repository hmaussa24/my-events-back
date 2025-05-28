# app/tests/functional/test_users_api.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

# Los fixtures 'client' y 'session' se importan automáticamente de conftest.py
# No necesitas un import explícito de pytest.fixture para usarlos en este archivo.

# Nuevas importaciones necesarias
from app.database.connection import get_db_session
from app.models.user import User

def test_create_user_api(client: TestClient):
    """
    Prueba el endpoint de creación de usuarios a través de la API.
    """
    user_data = {"email": "api_test@example.com", "password": "ApiTestPassword123"}
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert "id" in created_user
    assert created_user["is_active"] is True
    assert created_user["is_superuser"] is False
    assert "hashed_password" not in created_user # Aseguramos que el hash no se expone


def test_create_user_api_duplicate_email(client: TestClient):
    """
    Prueba que la creación de un usuario con email duplicado falla.
    """
    user_data = {"email": "duplicate@example.com", "password": "Password123"}
    client.post("/api/v1/users/", json=user_data) # Crea el primer usuario

    response = client.post("/api/v1/users/", json=user_data) # Intenta crear de nuevo

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_access_token(client: TestClient, test_user: dict):
    """
    Prueba el endpoint de login y la obtención de un token de acceso.
    """
    login_data = {"username": test_user.email, "password": "testpassword"} # OAuth2 espera 'username'
    response = client.post("/api/v1/login/access-token", data=login_data) # Usamos data= para form-urlencoded

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_read_users_me(client: TestClient, test_user: User):
    """
    Prueba el endpoint /users/me con un token válido.
    """
    # Primero, obtenemos un token para el usuario de prueba
    login_data = {"username": test_user.email, "password": "testpassword"}
    login_response = client.post("/api/v1/login/access-token", data=login_data)
    token = login_response.json()["access_token"]

    # Hacemos la solicitud a /users/me con el token
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    user_me = response.json()
    assert user_me["email"] == test_user.email
    assert user_me["id"] == test_user.id


def test_read_users_me_unauthorized(client: TestClient):
    """
    Prueba que /users/me devuelve 401 si no hay token.
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_read_user_by_id_as_superuser(client: TestClient, test_user: User, session: Session): # <-- ¡Cambia la firma aquí!
    """
    Prueba el endpoint /users/{user_id} con un superusuario.
    """
    from app.core.security import get_password_hash
    from app.models.user import User # Asegúrate de que User esté importado

    # Crear un superusuario de prueba
    superuser_password = get_password_hash("superpassword")
    superuser = User(email="super@example.com", hashed_password=superuser_password, is_superuser=True)

    # Usa la sesión directamente aquí, NO llames Session() de nuevo.
    session.add(superuser) # <--- ¡Cambiado!
    session.commit()       # <--- ¡Cambiado!
    session.refresh(superuser) # <--- ¡Cambiado!

    # Login como superusuario para obtener token
    login_data = {"username": superuser.email, "password": "superpassword"}
    login_response = client.post("/api/v1/login/access-token", data=login_data)
    token = login_response.json()["access_token"]

    # Imprime el token del superusuario para depuración (opcional, pero útil)
    print(f"Superuser Generated Token: {token}")

    # Intentar obtener el usuario de prueba por ID como superusuario
    response = client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200 # 

def test_read_user_by_id_as_normal_user(client: TestClient, test_user: User):
    """
    Prueba que un usuario normal no puede acceder a /users/{user_id}.
    """
    # Login como usuario normal para obtener token
    login_data = {"username": test_user.email, "password": "testpassword"}
    login_response = client.post("/api/v1/login/access-token", data=login_data)
    token = login_response.json()["access_token"]

    # Intentar obtener el usuario de prueba por ID como usuario normal
    response = client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert "The user doesn't have enough privileges" in response.json()["detail"]