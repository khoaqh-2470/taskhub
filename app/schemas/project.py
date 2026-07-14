from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.task import TaskWithTagsResponse


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_id: int | None = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime


class ProjectWithTasksResponse(ProjectResponse):
    tasks: list[TaskWithTagsResponse] = Field(default_factory=list)
