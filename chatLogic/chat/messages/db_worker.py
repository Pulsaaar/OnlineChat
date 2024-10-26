from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models import Message, User

async def get_messages_between_users(
    db: AsyncSession, sender_id: int, recipient_id: int
):
    stmt = select(Message).where(
        or_(
            (Message.sender_id == sender_id) & (Message.recipient_id == recipient_id),
            (Message.sender_id == recipient_id) & (Message.recipient_id == sender_id)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def add_message(
    db: AsyncSession, sender_id: int, recipient_id: int, content: str
):
    new_message = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    return new_message

async def get_all_user_ids_and_usernames(session: AsyncSession):
    result = await session.execute(select(User.id, User.email))
    return result.all()
