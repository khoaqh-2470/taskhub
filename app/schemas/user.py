from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.project import ProjectWithTasksResponse
from app.schemas.task import TaskWithTagsResponse


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    created_at: datetime


class UserProfileResponse(UserResponse):
    projects: list[ProjectWithTasksResponse] = Field(default_factory=list)
    assigned_tasks: list[TaskWithTagsResponse] = Field(default_factory=list)
