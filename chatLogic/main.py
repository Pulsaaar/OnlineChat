from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat.router import router as router_chat
from auth.router import router as router_auth

# Создаем экземпляр FastAPI
app = FastAPI()

# Определяем разрешенные источники для CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1"
]

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,   # Разрешить отправку учетных данных
    allow_methods=["*"],      # Разрешить все HTTP-методы
    allow_headers=["*"],      # Разрешить все заголовки
)

# Подключаем маршрутизаторы для чата и аутентификации
app.include_router(router_chat)  # Маршруты для чата
app.include_router(router_auth)   # Маршруты для аутентификации
