from fastapi import APIRouter, Depends
from db.workers.db_user import get_all_user_ids_and_usernames
from db.models import User

from db.database import get_async_session
from auth.authentication import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/users"
)

@router.get("/me/")
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