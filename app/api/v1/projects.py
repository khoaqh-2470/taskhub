from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import project as project_crud
from app.crud import task as task_crud
from app.crud import user as user_crud
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.task import TaskCreateInProject, TaskWithTagsResponse


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return project_crud.get_projects(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = project_crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project


@router.get("/{project_id}/tasks", response_model=list[TaskWithTagsResponse])
def read_project_tasks(project_id: int, db: Session = Depends(get_db)):
    db_project = project_crud.get_project_with_tasks(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project.tasks


@router.post(
    "/{project_id}/tasks",
    response_model=TaskWithTagsResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_task(
    project_id: int,
    task: TaskCreateInProject,
    db: Session = Depends(get_db),
):
    if project_crud.get_project(db, project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if task.assignee_id is not None and user_crud.get_user(db, task.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")

    return task_crud.create_task_in_project(db, project_id, task)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    owner = user_crud.get_user(db, project.owner_id)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner not found")
    return project_crud.create_project(db, project)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = project_crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.owner_id is not None and user_crud.get_user(db, project.owner_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner not found")

    return project_crud.update_project(db, db_project, project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = project_crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    project_crud.delete_project(db, db_project)
    return None
