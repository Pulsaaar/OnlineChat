from fastapi import FastAPI
from fastapi import Depends
from chat.router import router as router_chat
from auth.router import router as router_auth
from auth.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from chat.messages.db_worker import *
from fastapi.middleware.cors import CORSMiddleware
from models import User
from auth.auth_back import current_active_user

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_chat)
app.include_router(router_auth)

@app.get("/messages/")
async def get_messages(recipient_id: int, sender_id: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    messages = await get_messages_between_users(db, sender_id.id, recipient_id)
    return [{'id': message.id, 'sender_id': message.sender_id, 'recipient_id': message.recipient_id, 'content': message.content} for message in messages]

# # Пример использования в FastAPI:
# @app.post("/messages/")
# async def create_message(
#     sender_id: int, recipient_id: int, content: str, db: AsyncSession = Depends(get_async_session)
# ):
#     new_message = await add_message(db, sender_id, recipient_id, content)
#     return {"message_id": new_message.id, "content": new_message.content}
