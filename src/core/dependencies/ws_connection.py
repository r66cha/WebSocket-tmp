"""WebSocket Manager."""

# -- Imports

import logging
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket


# -- Exports

__all__ = [
    "manager",
    "get_ws_manager",
    "WSConnectionManager",
]

# --

log = logging.getLogger(__name__)

# --


class WSConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, "WebSocket"] = {}

    async def connect(self, user_id: int, websocket: "WebSocket"):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        log.info("User %s connected", user_id)

    async def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        log.info("User %s disconnected", user_id)

    async def send_personal_message(
        self, sender_id: int, receiver_id: int, message: str
    ):
        websocket = self.active_connections.get(receiver_id)
        if websocket:
            await websocket.send_text(f"From {sender_id}: {message}")
        else:
            log.warning("User %s is offline, store message in DB", receiver_id)
            # RabbitMQ safe


manager = WSConnectionManager()


# Dependency
def get_ws_manager() -> WSConnectionManager:
    return manager
