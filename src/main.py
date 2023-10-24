import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.routes import api_router
from src.core.config import settings
from src.core.errors.handlers import (
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    redoc_url="/docs",
    docs_url=None,
    title="Yurb",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


app.exception_handler(StarletteHTTPException)(http_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)


app.include_router(api_router)

if __name__ == "__main__":
    port = settings.port
    environment = settings.environment

    dev_mode = True if environment == "dev" else False

    uvicorn.run("main:app", port=port, reload=dev_mode, host="0.0.0.0")
