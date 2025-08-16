"""Main app router"""

# -- Imports

from fastapi import APIRouter
from src.api.routers.WebSocket import websocket_router

# -- Exports

__all__ = ["main_router"]

# --


main_router = APIRouter(prefix="/prefix")
# main_router.include_router(websocket_router)
