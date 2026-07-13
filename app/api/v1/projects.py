from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import project as project_crud
from app.crud import user as user_crud
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate


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
