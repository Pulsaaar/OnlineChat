from fastapi import WebSocket
import json
from celery_app import send_message_task
from db.workers.db_user import get_user_by_id
from db.workers.db_message import add_message

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, websocket: WebSocket):
        for user_id, connection in self.active_connections.items():
            if connection == websocket:
                del self.active_connections[user_id]
                break
        

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_private_message(self, message: str):
        message_data = json.loads(message) 
        sender_id = message_data['sender_id']
        receiver_id = message_data['recipient_id']
        content = message_data['content']
        receiver_socket = self.active_connections.get(receiver_id)

        await add_message(
               sender_id=sender_id, 
               recipient_id=receiver_id, 
               content=content
            )

        if receiver_socket:
            await receiver_socket.send_text(message)
        else:
            user = await get_user_by_id(receiver_id)
            send_message_task.delay(user.telegram_id, f"{user.email}: {content}")


manager = ConnectionManager()