from pydantic import BaseModel, ConfigDict


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
