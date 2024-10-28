from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .conn_manager import manager
from .messages.router import router as router_msg 
from .users.router import router as router_users

# Создаем основной маршрутизатор для чата с префиксом "/chat"
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# Включаем маршруты для сообщений
router.include_router(router_msg)
router.include_router(router_users)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: int, 
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
