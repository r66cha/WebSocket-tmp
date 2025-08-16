"""Main app router"""

# -- Imports

from fastapi import APIRouter
from src.api.routers.Websocket import websocket_router

# -- Exports

__all__ = ["main_router"]

# --


main_router = APIRouter(prefix="/ws")
main_router.include_router(websocket_router)
