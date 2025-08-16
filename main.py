"""Application entry point."""

# -- Imports

import uvicorn
import logging
from src.api.app import app
from src.core.log import conf_logging

# --

HOST = "0.0.0.0"
PORT = 8000

# --


if __name__ == "__main__":

    conf_logging(level=logging.INFO)

    uvicorn.run(
        app=app,
        host=HOST,
        port=PORT,
        reload=True,
    )
