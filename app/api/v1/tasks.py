from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import project as project_crud
from app.crud import task as task_crud
from app.crud import user as user_crud
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return task_crud.get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if project_crud.get_project(db, task.project_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found")

    if task.assignee_id is not None and user_crud.get_user(db, task.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")

    return task_crud.create_task(db, task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if task.project_id is not None and project_crud.get_project(db, task.project_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found")

    if task.assignee_id is not None and user_crud.get_user(db, task.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")

    return task_crud.update_task(db, db_task, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_crud.delete_task(db, db_task)
    return None
