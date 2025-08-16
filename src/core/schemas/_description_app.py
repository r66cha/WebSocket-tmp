"""Description App."""

# -- Imports

from pydantic import BaseModel

# -- Exports

__all__ = ["DescriptionAppSchema"]

#


class DescriptionAppSchema(BaseModel):
    title: str = "WebsocketTMP-Service"
    description: str = "Websocket template"
    version: str = "1.0.0"
