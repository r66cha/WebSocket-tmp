"""Application entry point."""

# -- Imports

import uvicorn


# --

HOST = "0.0.0.0"
PORT = 8080
APP = "src.api.app:app"

# --


if __name__ == "__main__":

    uvicorn.run(
        app=APP,
        host=HOST,
        port=PORT,
        reload=True,
    )
