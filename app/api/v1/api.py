# app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import users # Importamos los routers de nuestros endpoints

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"]) # Montamos el router de usuarios
# Puedes añadir más routers aquí a medida que los crees, por ejemplo:
# from app.api.v1.endpoints import items
# api_router.include_router(items.router, prefix="/items", tags=["items"])