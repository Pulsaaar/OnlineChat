from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models import Message, User
from auth.database import get_async_session
from typing import Optional

async def get_messages_between_users(
    db: AsyncSession, sender_id: int, recipient_id: int
) -> list[Message]:
    """
    Получаем сообщения между двумя пользователями по их идентификаторам.

    :param db: Асинхронная сессия базы данных
    :param sender_id: Идентификатор отправителя
    :param recipient_id: Идентификатор получателя
    :return: Список сообщений между пользователями
    """
    # Формируем SQL-запрос для выборки сообщений между двумя пользователями
    stmt = select(Message).where(
        or_(
            (Message.sender_id == sender_id) & (Message.recipient_id == recipient_id),
            (Message.sender_id == recipient_id) & (Message.recipient_id == sender_id)
        )
    )
    
    # Выполняем запрос и возвращаем все сообщения
    result = await db.execute(stmt)
    return result.scalars().all()

async def add_message(
    sender_id: int, recipient_id: int, content: str
) -> Message:
    """
    Добавляем новое сообщение в базу данных.

    :param sender_id: Идентификатор отправителя
    :param recipient_id: Идентификатор получателя
    :param content: Содержимое сообщения
    :return: Созданное сообщение
    """
    # Создаем новый объект сообщения
    new_message = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content
    )
    
    # Добавляем сообщение в базу данных
    async for session in get_async_session():
        session.add(new_message)
        await session.commit()  # Сохраняем изменения
        await session.refresh(new_message)  # Обновляем объект с новыми данными из базы
    
    return new_message  # Возвращаем созданное сообщение

async def get_all_user_ids_and_usernames(
    db: AsyncSession, exclude_user_id: int
) -> list[tuple[int, str]]:
    """
    Получаем список идентификаторов и email всех пользователей, кроме указанного.

    :param db: Асинхронная сессия базы данных
    :param exclude_user_id: Идентификатор пользователя, которого нужно исключить
    :return: Список кортежей с идентификаторами и email
    """
    # Выполняем SQL-запрос для получения пользователей, исключая указанный идентификатор
    result = await db.execute(select(User.id, User.email).where(User.id != exclude_user_id))
    
    # Возвращаем все результаты запроса
    return result.all()


async def get_user_by_id(user_id: int) -> Optional[User]:
    async for session in get_async_session():
        # Выполнение асинхронного запроса для получения пользователя по id
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем первого пользователя или None

        return user
