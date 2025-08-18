"""WebSocket client."""

# -- Imports

import asyncio
import websockets
import logging
from datetime import datetime, timezone


# --

log = logging.getLogger(__name__)

# --


# Echo
async def echo_client():
    uri = "ws://127.0.0.1:8080/ws/echo"
    try:
        async with websockets.connect(uri=uri) as ws:
            await ws.send("Hello Echo!")
            response = await ws.recv()
            log.info("Echo response: %s", response)
    except Exception as e:
        log.warning("Exception: %s", e)


# Private chat
async def private_chat_client(me: int, receiver: int):
    uri = f"ws://127.0.0.1:8080/ws/chats/{receiver}"

    try:
        async with websockets.connect(
            uri=uri,
            additional_headers=[("Cookie", f"me={me}")],
        ) as ws:
            await ws.send("Hello!")
            response = await ws.recv()
            log.info("Private chat response: %s", response)
    except Exception as e:
        log.warning("Exception: %s", e)


# Multichat
async def multichat_client(me: int, room_id: int):
    uri = f"ws://127.0.0.1:8080/ws/rooms/{room_id}"

    try:
        async with websockets.connect(
            uri=uri,
            additional_headers=[("Cookie", f"me={me}")],
        ) as ws:
            await ws.send("Hello Room!")
            while True:
                timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                response = await ws.recv()
                log.info(
                    f"[{timestamp}] [Room {room_id}] [User {me}] message:", response
                )
    except Exception as e:
        log.warning("Exception: %s", e)


async def main():
    await echo_client()
    await private_chat_client(me=1, receiver=2)
    # await multichat_client(me=1, room_id=27)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.warning("Close connection")
