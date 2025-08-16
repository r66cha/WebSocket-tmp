"""FastAPI application instance."""

# -- Imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.routers._0_main_router import main_router
from fastapi.responses import ORJSONResponse


# -- Exports

__all__ = ["app"]

# --


def getUP() -> FastAPI:
    app = FastAPI(
        title=settings._description.title,
        description=settings._description.description,
        version=settings._description.version,
        default_response_class=ORJSONResponse,
        docs_url="/docs",
    )

    # Routers
    app.include_router(main_router)

    # Middleware
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
    )

    return app


app = getUP()
