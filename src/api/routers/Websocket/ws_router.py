"""Websocket router."""

# -- Imports

import logging
from fastapi import APIRouter, WebSocket

# -- Exports

__all__ = ["ws_router"]

# --

ws_router = APIRouter()
log = logging.getLogger(__name__)

# --


@ws_router.websocket(path="/ws", name="Websocket-tmp")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        log.info("Data: %s", data)
        await websocket.send_text(f"You sent: {data}")
