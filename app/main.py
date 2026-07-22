import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import projects, tasks, users
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import register_middlewares


logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "users", "description": "User registration, login, profile, and admin user management."},
    {"name": "projects", "description": "Project CRUD and project task collection endpoints."},
    {"name": "tasks", "description": "Task CRUD with project ownership authorization."},
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logger.info("%s is starting", settings.app_name)
    yield
    logger.info("%s is shutting down", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="TaskHub REST API for users, projects, tasks, authentication, and authorization.",
    version="0.7.0",
    debug=settings.debug,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)
register_middlewares(app)
register_exception_handlers(app)

app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskHub API"}
