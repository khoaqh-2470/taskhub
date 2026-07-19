from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tag import TagResponse


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"
    due_date: date | None = None


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: int | None = None


class TaskCreateInProject(TaskBase):
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    project_id: int | None = None
    assignee_id: int | None = None
    due_date: date | None = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    assignee_id: int | None = None
    created_at: datetime


class TaskWithTagsResponse(TaskResponse):
    tags: list[TagResponse] = Field(default_factory=list)
