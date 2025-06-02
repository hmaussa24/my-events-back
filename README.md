# My Events Back

Backend de gestión de eventos desarrollado con FastAPI, PostgreSQL y Docker.

## Arquitectura del Proyecto

Este backend está construido siguiendo una arquitectura modular y desacoplada, facilitando la escalabilidad, el mantenimiento y la extensibilidad. Los principales componentes son:

### 1. API (FastAPI)
- **Ubicación:** `app/api/`
- Expone los endpoints RESTful organizados por versión (`v1`) y por dominio (eventos, sesiones, usuarios, registros).
- Incluye documentación automática Swagger y Redoc.

### 2. Modelos y Esquemas
- **Modelos (ORM):** `app/models/`
  - Definen la estructura de las tablas en la base de datos usando SQLAlchemy.
- **Esquemas (Pydantic):** `app/schemas/`
  - Validan y serializan los datos de entrada/salida de la API.

### 3. Casos de Uso (Use Cases)
- **Ubicación:** `app/use_cases/`
- Implementan la lógica de negocio para cada operación (crear sesión, registrar usuario, etc.), separando la lógica de la capa de presentación (API).

### 4. Repositorios
- **Ubicación:** `app/repositories/`
- Encapsulan el acceso a la base de datos, permitiendo cambiar la fuente de datos sin afectar la lógica de negocio.

### 5. Configuración y Utilidades
- **Configuración:** `app/core/config.py` y `.env`
  - Manejo de variables de entorno y configuración global.
- **Seguridad:** `app/core/security.py`
  - Autenticación JWT, manejo de contraseñas y tokens.
- **Excepciones y logging:** `app/core/exceptions.py`, `app/core/logging_config.py`

### 6. Migraciones
- **Ubicación:** `app/database/migrations/` (Alembic)
- Migraciones automáticas aplicadas al iniciar el backend vía Docker Compose.

### 7. Archivos Estáticos
- **Ubicación:** `static/`
- Almacena imágenes de eventos y otros recursos estáticos, servidos por FastAPI.

### 8. Contenedores y Orquestación
- **Dockerfile:** Define la imagen del backend.
- **docker-compose.yml:** Orquesta el backend y la base de datos PostgreSQL, asegurando persistencia y ejecución de migraciones.

---

# Instrucciones de Ejecución

## Requisitos
- Docker
- Docker Compose

## Configuración
1. Clona el repositorio y entra en la carpeta del proyecto.
2. Edita el archivo `.env` si necesitas cambiar credenciales o configuraciones.

## Ejecución rápida
Levanta la API y la base de datos (las migraciones se aplican automáticamente):

```sh
docker-compose up --build
```

- La API estará disponible en: http://localhost:8000
- La base de datos PostgreSQL estará en: localhost:5433

## Endpoints principales
- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

## Estructura del proyecto
- `app/` Código fuente principal
- `static/` Archivos estáticos (imágenes de eventos)
- `alembic/` Migraciones de base de datos

## Notas
- Las migraciones de Alembic se ejecutan automáticamente al iniciar el backend.
- Los archivos estáticos se sirven desde `/static`.
- Para desarrollo local sin Docker, asegúrate de tener PostgreSQL corriendo y configura el `.env` acorde.

## Comandos útiles
- Parar los servicios:
  ```sh
  docker-compose down
  ```
- Ver logs:
  ```sh
  docker-compose logs -f
  ```

---

Cualquier duda, revisa la documentación de los endpoints o consulta al responsable del proyecto.
