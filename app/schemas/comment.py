from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int
    user_id: int


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user_id: int
    created_at: datetime
