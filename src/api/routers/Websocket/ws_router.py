"""Websocket router."""

# -- Imports

import logging
from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Cookie, Depends

from src.core.dependencies import WSConnectionManager, get_ws_manager
from typing import Set, Annotated, TYPE_CHECKING


# -- Exports

__all__ = ["websocket_router"]

# --

websocket_router = APIRouter()
log = logging.getLogger(__name__)

clients: Set[WebSocket] = set()

# --


# Default tmp for WebSOcket
@websocket_router.websocket(
    path="/ws/default",
    name="Websocket-tmp-default",
)
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


@websocket_router.websocket(
    path="/ws/chats/{receiver_id}",
    name="Websocket-tmp-personal_chat",
)
async def private_chat(
    websocket: WebSocket,
    manager: Annotated[WSConnectionManager, Depends(get_ws_manager)],
    receiver_id: int,
    sender_id: Annotated[int | None, Cookie(alias="me")] = None,
):
    if sender_id is None:
        await websocket.close(code=4001)  # или возвращаем ошибку
        return

    try:
        await manager.connect(sender_id, websocket)
        while True:
            try:
                message = await websocket.receive_text()
                log.info("Received from %s: %s", sender_id, message)
                await manager.send_personal_message(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    message=message,
                )
            except WebSocketDisconnect:
                log.info("User %s disconnected during message receive", sender_id)
                break
            except Exception as e:
                log.error("Error handling message from user %s: %s", sender_id, e)

    except WebSocketDisconnect:
        log.info("User %s disconnected", sender_id)
    except Exception as e:
        log.error("Unexpected exception for user %s: %s", sender_id, e)
    finally:
        await manager.disconnect(sender_id)
        log.info("Connection with user %s cleaned up", sender_id)
