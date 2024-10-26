from fastapi import WebSocket
from .celery.tasks import notify_user
import json
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_private_message(self, message: str, receiver_id: int):
        receiver_socket = self.active_connections.get(receiver_id)
        if receiver_socket:
            await receiver_socket.send_text(message)
        #else:
        #    message = json.loads(message)
        #    print(f"{message['content']}")
        #    notify_user.delay(id, message['content'])


manager = ConnectionManager()