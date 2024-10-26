from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from .conn_manager import manager
from auth.auth_back import current_active_user
from auth.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from chat.messages.db_worker import *
import json

router = APIRouter(
    prefix="/chat",
    tags=["Chat"])

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data) 
            receiver_id = message_data['recipient_id']
            message = message_data['content']
            await manager.send_private_message(data, receiver_id)
            # await manager.send_message(f"You wrote {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{client_id} left the chat")


@router.post("/messages/")
async def create_message(
    recipient_id: int, content: str, sender: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)
):
    new_message = await add_message(db, sender.id, recipient_id, content)
    return {"message_id": new_message.id, "content": new_message.content}


@router.get("/users/")
async def get_users(db: AsyncSession = Depends(get_async_session)):
    new_message = await get_all_user_ids_and_usernames(db)
    return [{"id": user_id, "username": username} for user_id, username in new_message]

@router.get("/me/")
async def get_me(sender: User = Depends(current_active_user)):
    return {'id': sender.id, 'email': sender.email}
