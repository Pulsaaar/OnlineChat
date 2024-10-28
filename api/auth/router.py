from fastapi import APIRouter
from .authentication import auth_backend, fastapi_users
from .schemas import UserCreate, UserRead

# Создаем маршрутизатор для аутентификации
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Включаем маршруты для аутентификации
router.include_router(
    fastapi_users.get_auth_router(auth_backend),  # Маршруты для аутентификации пользователей
)

# Включаем маршруты для регистрации
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)  # Маршруты для регистрации новых пользователей
)
