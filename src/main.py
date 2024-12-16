from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from controllers import api_router
from database.connection import client

app = FastAPI(debug=True)

app.include_router(api_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import debugpy

    debugpy.listen(("0.0.0.0", 8451))

    uvicorn_run(
        "main:app",
        host="0.0.0.0",
        port=8400,
        log_level="info",
        reload=True,
        workers=1,
    )
