from sys import path as sys_path
from os import getcwd as os_getcwd

# Adding ./src to python path for running from console purpose:
sys_path.append(os_getcwd())

from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from src.lifespan import lifespan
from src.apis.routes import router as main_router
from src.constants import API_DOC_METADATA

app: FastAPI = FastAPI(
    lifespan=lifespan,
    # API METADATA
    title=API_DOC_METADATA["title"],
    description=API_DOC_METADATA["description"],
    version=API_DOC_METADATA["version"],
)
# При необходимости можно настроить CORS
# app.add_middleware()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn_run(app=app, host="0.0.0.0", port=8000)
