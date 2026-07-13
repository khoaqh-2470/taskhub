from typing import Annotated

from fastapi import Depends


ProjectStore = list[dict[str, object]]

project_store: ProjectStore = [
    {
        "id": 1,
        "name": "TaskHub API",
        "description": "Build the FastAPI skeleton",
        "owner_id": 1,
    }
]


def get_project_store() -> ProjectStore:
    return project_store


ProjectStoreDep = Annotated[ProjectStore, Depends(get_project_store)]
