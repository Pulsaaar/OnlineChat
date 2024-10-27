from fastapi import APIRouter, Depends
from auth.auth_back import current_active_user
from auth.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from .db_worker import add_message, get_messages_between_users

# Создаем маршрутизатор для работы с сообщениями
router = APIRouter(
    prefix="/messages"
)

@router.post("/")
async def create_message(
    recipient_id: int, 
    content: str, 
    sender: User = Depends(current_active_user), 
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создаем новое сообщение.

    :param recipient_id: Идентификатор получателя
    :param content: Содержимое сообщения
    :param sender: Текущий активный пользователь (отправитель)
    :param db: Асинхронная сессия базы данных
    :return: Словарь с идентификатором сообщения и его содержимым
    """
    # Добавляем сообщение в базу данных
    new_message = await add_message(db, sender.id, recipient_id, content)
    
    # Возвращаем информацию о созданном сообщении
    return {"message_id": new_message.id, "content": new_message.content}

@router.get("/")
async def get_messages(
    recipient_id: int, 
    sender: User = Depends(current_active_user), 
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получаем все сообщения между текущим пользователем и указанным получателем.

    :param recipient_id: Идентификатор получателя
    :param sender: Текущий активный пользователь (отправитель)
    :param db: Асинхронная сессия базы данных
    :return: Список сообщений в виде словарей
    """
    # Получаем сообщения между пользователями
    messages = await get_messages_between_users(db, sender.id, recipient_id)
    
    # Формируем и возвращаем список сообщений
    return [
        {
            'id': message.id, 
            'sender_id': message.sender_id, 
            'recipient_id': message.recipient_id, 
            'content': message.content
        } 
        for message in messages
    ]
