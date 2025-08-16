"""FastAPI application instance."""

# -- Imports

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.api.routers.WebSocket import websocket_router
from fastapi.responses import ORJSONResponse
from src.core.log import conf_logging


# -- Exports

__all__ = ["app"]

# --


def getUP() -> FastAPI:

    conf_logging(level=logging.INFO)

    app = FastAPI(
        title=settings._description.title,
        description=settings._description.description,
        version=settings._description.version,
        default_response_class=ORJSONResponse,
        docs_url="/docs",
    )

    # Routers
    app.include_router(websocket_router)

    # Middleware
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = getUP()
