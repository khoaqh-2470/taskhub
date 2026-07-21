from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.crud import project as project_crud
from app.crud import task as task_crud
from app.crud import user as user_crud
from app.models.project import Project
from app.models.task import Task
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN_ROLE = "admin"


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    db_user = user_crud.get_user_by_username(db, username)
    if db_user is None:
        raise credentials_exception
    return db_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return current_user


def can_manage_project(current_user: User, project: Project) -> bool:
    return current_user.role == ADMIN_ROLE or project.owner_id == current_user.id


def get_project_for_owner_or_admin(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    db_project = project_crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not can_manage_project(current_user, db_project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return db_project


def get_task_for_project_owner_or_admin(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db_project = project_crud.get_project(db, db_task.project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not can_manage_project(current_user, db_project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    return db_task
