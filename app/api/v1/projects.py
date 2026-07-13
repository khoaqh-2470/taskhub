from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import ProjectStoreDep
from app.crud import project as project_crud
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def read_projects(projects: ProjectStoreDep, skip: int = 0, limit: int = 100):
    return project_crud.get_projects(projects, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, projects: ProjectStoreDep):
    db_project = project_crud.get_project(projects, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, projects: ProjectStoreDep):
    return project_crud.create_project(projects, project)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, projects: ProjectStoreDep):
    db_project = project_crud.get_project(projects, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project_crud.update_project(db_project, project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, projects: ProjectStoreDep):
    db_project = project_crud.get_project(projects, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    project_crud.delete_project(projects, db_project)
    return None
