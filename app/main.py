from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router as api_router
from app.dependencies import get_task_repository
from app.modules.tasks import handlers  # noqa: F401 — triggers @task_handler decorators
from app.modules.tasks.utils import register_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_handlers(get_task_repository())
    yield


app = FastAPI(
    title="Flow Manager", version="0.1.0", lifespan=lifespan, redirect_slashes=True
)

app.include_router(api_router)
