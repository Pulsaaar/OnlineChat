from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .conn_manager import manager
from auth.auth_back import current_active_user
from models import User
from auth.database import get_async_session
from celery_app import send_message_task
from sqlalchemy.ext.asyncio import AsyncSession
import json
from .messages.db_worker import get_all_user_ids_and_usernames
from .messages.router import router as router_msg 

# Создаем основной маршрутизатор для чата с префиксом "/chat"
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# Включаем маршруты для сообщений
router.include_router(router_msg)

@router.get("/users/me/")
async def get_users_and_me(
    db: AsyncSession = Depends(get_async_session), 
    sender: User = Depends(current_active_user)
):
    """
    Получаем данные текущего пользователя и список всех пользователей.
    """
    # Получаем идентификаторы и email всех пользователей
    users = await get_all_user_ids_and_usernames(db, sender.id)
    
    # Формируем данные для текущего пользователя
    me_data = {"id": sender.id, "email": sender.email}
    
    return {
        "me": me_data,
        "users": [{"id": user_id, "email": email} for user_id, email in users]
    }

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: int, 
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обрабатываем подключение к WebSocket для отправки и получения сообщений.
    """
    await manager.connect(websocket, client_id)  # Подключаем клиента
    try:
        while True:
            # Получаем данные от клиента
            data = await websocket.receive_text()
            
            # Отправляем личное сообщение получателю
            await manager.send_private_message(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)  # Отключаем клиента при разрыве соединения
