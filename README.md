# My Events Back

Backend de gestión de eventos desarrollado con FastAPI, PostgreSQL y Docker.

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
