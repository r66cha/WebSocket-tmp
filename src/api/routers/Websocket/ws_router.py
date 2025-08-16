"""Websocket router."""

# -- Imports

import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set

# -- Exports

__all__ = ["websocket_router"]

# --

websocket_router = APIRouter()
log = logging.getLogger(__name__)

clients: Set[WebSocket] = set()

# --


@websocket_router.websocket(path="/", name="Websocket-tmp")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            log.info("Data: %s", data)
            for client in clients:
                await client.send_text(f"You sent: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)
        log.warning("Client disconnected")
    except Exception as e:
        clients.remove(websocket)
        log.error("Unexpected exception in websocket: %s", e)
