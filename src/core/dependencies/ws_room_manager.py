"""WebSocket Manager."""

# -- Imports

import logging
from typing import Dict, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket


# -- Exports

__all__ = [
    "room_manager",
    "get_ws_room_manager",
    "WSRoomConnectionManager",
]

# --

log = logging.getLogger(__name__)

# --


class WSRoomConnectionManager:
    def __init__(self):
        # room_id -> set of websockets
        self.rooms: Dict[int, Set["WebSocket"]] = {}

    async def connect(
        self,
        room_id: int,
        websocket: "WebSocket",
    ):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(websocket)
        log.info("Client joined room %s", room_id)

    async def disconnect(
        self,
        room_id: int,
        websocket: "WebSocket",
    ):
        if room_id in self.rooms:
            self.rooms[room_id].discard(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
        log.info("Client left room %s", room_id)

    async def broadcast(
        self,
        sender_ws: "WebSocket",
        room_id: int,
        message: str,
    ):
        connections = self.rooms.get(room_id, set())
        disconnected = []

        for ws in connections:
            if ws is sender_ws:
                continue
            try:
                await ws.send_text(message)
            except Exception as e:
                log.error("Failed to send to room %s: %s", room_id, e)
                disconnected.append(ws)

        for ws in disconnected:
            connections.remove(ws)
            log.info("Removed dead connection from room %s", room_id)


room_manager = WSRoomConnectionManager()


# Dependency
def get_ws_room_manager() -> WSRoomConnectionManager:
    return room_manager
