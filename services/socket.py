from fastapi import WebSocket
from typing import List


class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def is_alive(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class SocketEvents():
    ADD_ROOM = "ADD_ROOM"
    REMOVE_ROOM = "REMOVE_ROOM"
    ADD_DEVICE = "ADD_DEVICE"
    SWITCH_DEVICE = "SWITCH_DEVICE"
    SCHEDULED_SWITCH_DEVICE = "SCHEDULED_SWITCH_DEVICE"
    CONFIGURE_DEVICE = "CONFIGURE_DEVICE"
    REMOVE_DEVICE = "REMOVE_DEVICE"
    USER_LEFT = "USER_LEFT"
    ENERGY_CONSUMPTION_CALCULATED = "ENERGY_CONSUMPTION_CALCULATED"
