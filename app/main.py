from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import projects, tasks, users
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.middleware import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print(f"{settings.app_name} is starting")
    yield
    print(f"{settings.app_name} is shutting down")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
register_middlewares(app)
register_exception_handlers(app)

app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskHub API"}
