from fastapi import WebSocket
import json
# from aiogram import Bot
# from config import API_TOKEN

# API_TOKEN = API_TOKEN 
# bot = Bot(token=API_TOKEN)


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
        # else:
        #     message = json.loads(message)
        #     await bot.send_message("@Pulsaar", message['content'])


manager = ConnectionManager()