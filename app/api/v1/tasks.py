from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import can_manage_project, get_current_user, get_task_for_project_owner_or_admin
from app.core.cache import delete_cache_key, project_tasks_cache_key
from app.core.database import get_db
from app.crud import project as project_crud
from app.crud import task as task_crud
from app.crud import user as user_crud
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse], summary="List tasks")
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return task_crud.get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse, summary="Get task detail")
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_project = project_crud.get_project(db, task.project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found")

    if not can_manage_project(current_user, db_project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    if task.assignee_id is not None and user_crud.get_user(db, task.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")

    db_task = task_crud.create_task(db, task)
    delete_cache_key(project_tasks_cache_key(task.project_id))
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task: TaskUpdate,
    db_task: Task = Depends(get_task_for_project_owner_or_admin),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_project_id = db_task.project_id
    if task.project_id is not None:
        db_project = project_crud.get_project(db, task.project_id)
        if db_project is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found")
        if not can_manage_project(current_user, db_project):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    if task.assignee_id is not None and user_crud.get_user(db, task.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")

    updated_task = task_crud.update_task(db, db_task, task)
    delete_cache_key(project_tasks_cache_key(old_project_id))
    delete_cache_key(project_tasks_cache_key(updated_task.project_id))
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    db_task: Task = Depends(get_task_for_project_owner_or_admin),
    db: Session = Depends(get_db),
):
    project_id = db_task.project_id
    task_crud.delete_task(db, db_task)
    delete_cache_key(project_tasks_cache_key(project_id))
    return None
