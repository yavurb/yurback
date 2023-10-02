from fastapi import FastAPI
import uvicorn

from core.config import settings
from api import api_router

app = FastAPI(redoc_url="/docs", docs_url=None)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


app.include_router(api_router)

if __name__ == "__main__":
    port = settings.port
    environment = settings.environment

    dev_mode = True if environment == "dev" else False

    uvicorn.run("main:app", port=port, reload=dev_mode)