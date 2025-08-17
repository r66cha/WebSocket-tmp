"""Websocket router."""

# -- Imports

import logging
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    WebSocketDisconnect,
    WebSocket,
    Cookie,
    Path,
    Depends,
)

from src.core.dependencies import (
    WSChatConnectionManager,
    WSRoomConnectionManager,
    get_ws_chat_manager,
    get_ws_room_manager,
)
from typing import Set, Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket


# -- Exports

__all__ = ["websocket_router"]

# --

websocket_router = APIRouter()

log = logging.getLogger(__name__)

clients: Set[WebSocket] = set()


# --


# Echo
@websocket_router.websocket(
    path="/ws/echo",
    name="Websocket-tmp-echo",
)
async def echo(websocket: "WebSocket"):
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


# Private Chat
@websocket_router.websocket(
    path="/ws/chats/{receiver_id}",
    name="Websocket-tmp-personal_chat",
)
async def private_chat(
    websocket: "WebSocket",
    manager: Annotated[WSChatConnectionManager, Depends(get_ws_chat_manager)],
    receiver_id: Annotated[int, Path()],
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


# MultiChat
@websocket_router.websocket(
    path="/ws/rooms/{room_id}",
    name="Websocket-tmp-multichat",
)
async def multichat(
    websocket: "WebSocket",
    room_id: int,
    manager: Annotated[WSRoomConnectionManager, Depends(get_ws_room_manager)],
    sender_id: Annotated[int | None, Cookie(alias="me")] = None,
):
    if sender_id is None:
        await websocket.close(code=4001)
        return

    try:
        await manager.connect(room_id, websocket)
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            log.info("Room %s message: %s", room_id, data)
            await manager.broadcast(
                websocket,
                room_id,
                message=f"[{timestamp}] [Room {room_id}] [User {sender_id}]: {data}",
            )
    except WebSocketDisconnect:
        log.info("Client disconnected from room %s", room_id)
    except Exception as e:
        log.error("Unexpected error in room %s: %s", room_id, e)
    finally:
        await manager.disconnect(room_id, websocket)
