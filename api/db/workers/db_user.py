from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from typing import Optional
from db.database import get_async_session


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
